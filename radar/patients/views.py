from datetime import datetime

from flask import render_template, Blueprint, abort, request, url_for, redirect, session, flash
from flask_login import current_user

from radar.database import db
from radar.disease_groups.models import DiseaseGroup
from radar.models import UnitPatient, DiseaseGroupPatient
from radar.patients.models import Patient, Demographics
from radar.ordering import Ordering
from radar.pagination import paginate_query
from radar.patients.forms import PatientSearchForm, PER_PAGE_DEFAULT, PER_PAGE_CHOICES, DemographicsForm, \
    RecruitPatientSearchForm, RecruitPatientRadarForm, RecruitPatientRdcForm, PatientDiseaseGroupForm, PatientUnitForm
from radar.patients.recruit import find_existing_radar_patients, find_existing_rdc_patients
from radar.patients.sda import demographics_to_sda_bundle
from radar.patients.search import PatientQueryBuilder
from radar.sda.models import SDAPatient
from radar.patients.search import get_disease_group_filters_for_user, get_unit_filters_for_user
from radar.units.models import Unit
from radar.utils import get_path_as_text


bp = Blueprint('patients', __name__)


def get_patient_data(patient):
    units = sorted(patient.filter_units_for_user(current_user), key=lambda x: x.unit.name.lower())
    disease_groups = sorted(patient.filter_disease_groups_for_user(current_user), key=lambda x: x.disease_group.name.lower())

    return dict(
        units=units,
        disease_groups=disease_groups,
    )


@bp.route('/')
def view_patient_list():
    if not current_user.has_view_patient_permission:
        abort(403)

    form = PatientSearchForm(formdata=request.args, csrf_enabled=False)

    disease_group_choices = [(x.id, x.name) for x in get_disease_group_filters_for_user(current_user)]
    disease_group_choices.insert(0, ('', ''))
    form.disease_group_id.choices = disease_group_choices

    unit_choices = [(x.id, x.name) for x in get_unit_filters_for_user(current_user)]
    unit_choices.insert(0, ('', ''))
    form.unit_id.choices = unit_choices

    builder = PatientQueryBuilder(current_user)

    if form.validate():
        if form.first_name.data:
            builder.first_name(form.first_name.data)

        if form.last_name.data:
            builder.last_name(form.last_name.data)

        if form.unit_id.data:
            unit = Unit.query.get_or_404(form.unit_id.data)
            builder.unit(unit)

        if form.disease_group_id.data:
            disease_group = DiseaseGroup.query.get_or_404(form.disease_group_id.data)
            builder.disease_group(disease_group)

        if form.date_of_birth.data:
            builder.date_of_birth(form.date_of_birth.data)

        if form.patient_number.data:
            builder.patient_number(form.patient_number.data)

        if form.gender.data:
            builder.gender(form.gender.data)

        if form.radar_id.data:
            builder.radar_id(form.radar_id.data)

        if form.year_of_birth.data:
            builder.year_of_birth(form.year_of_birth.data)

        builder.order_by(form.order_by.data, form.order_direction.data)

    query = builder.build()

    ordering = Ordering(form.order_by.data, form.order_direction.data)
    pagination = paginate_query(query, default_per_page=PER_PAGE_DEFAULT)
    patients = pagination.items

    patients = [(x, get_patient_data(x)) for x in patients]

    context = dict(
        patients=patients,
        form=form,
        pagination=pagination,
        ordering=ordering,
        per_page_choices=PER_PAGE_CHOICES,
        disease_group_choices=disease_group_choices,
        unit_choices=unit_choices,
    )

    return render_template('patients.html', **context)


@bp.route('/<int:patient_id>/', endpoint='view_demographics_list')
@bp.route('/<int:patient_id>/', endpoint='view_patient')
def view_demographics_list(patient_id):
    patient = Patient.query.get_or_404(patient_id)

    if not patient.can_view(current_user):
        abort(403)

    sda_patients = SDAPatient.query\
        .join(SDAPatient.sda_bundle)\
        .join(Patient)\
        .filter(Patient.id == patient_id)\
        .all()

    demographics_list = []

    for sda_patient in sda_patients:
        demographics = dict()

        demographics['facility'] = sda_patient.sda_bundle.facility
        demographics['first_name'] = sda_patient.first_name
        demographics['last_name'] = sda_patient.last_name
        demographics['date_of_birth'] = sda_patient.date_of_birth
        demographics['date_of_death'] = sda_patient.date_of_death

        if sda_patient.gender == 'M':
            demographics['gender'] = 'Male'
        else:
            demographics['gender'] = 'Female'

        demographics['addresses'] = []

        # Sort by to time
        addresses = sorted(sda_patient.addresses, key=lambda x: (x.to_time or datetime.max), reverse=True)

        for address in addresses:
            demographics['addresses'].append({
                'from_time': address.from_time,
                'to_time': address.to_time,
                'address': address.full_address
            })

        demographics['aliases'] = []

        for alias in sda_patient.aliases:
            demographics['aliases'].append({
                'first_name': alias.first_name,
                'last_name': alias.last_name,
            })

        demographics['numbers'] = []

        numbers = sorted(sda_patient.numbers, key=lambda x: get_path_as_text(x.data, ['organization', 'description']))

        for number in numbers:
            demographics['numbers'] = [{
                'organization': get_path_as_text(number.data, ['organization', 'description']),
                'number': get_path_as_text(number.data, ['number']),
                'number_type': get_path_as_text(number.data, ['number_type'])
            }]

        demographics_list.append(demographics)

    context = dict(
        patient=patient,
        patient_data=get_patient_data(patient),
        demographics_list=demographics_list
    )

    return render_template('patient/demographics.html', **context)


@bp.route('/<int:patient_id>/radar/', endpoint='view_radar_demographics')
@bp.route('/<int:patient_id>/radar/', endpoint='edit_radar_demographics', methods=['POST'])
def view_radar_demographics(patient_id):
    patient = Patient.query.get_or_404(patient_id)
    demographics = Demographics.query.filter(Demographics.patient == patient).with_for_update(read=True).first()

    if demographics is None:
        demographics = Demographics(patient=patient)

    if not demographics.can_view(current_user):
        abort(403)

    read_only = not demographics.can_edit(current_user)

    form = DemographicsForm(obj=demographics)

    if request.method == 'POST':
        if read_only:
            abort(403)

        if form.validate():
            form.populate_obj(demographics)
            save_radar_demographics(demographics)
            db.session.add(demographics)
            db.session.commit()
            return redirect(url_for('patients.view_demographics_list', patient_id=demographics.patient.id))

    context = dict(
        patient=demographics.patient,
        patient_data=get_patient_data(demographics.patient),
        demographics=demographics,
        form=form,
        read_only=read_only
    )

    return render_template('patient/radar_demographics.html', **context)


@bp.route('/<int:patient_id>/disease-groups/', endpoint='view_patient_disease_groups')
@bp.route('/<int:patient_id>/disease-groups/', endpoint='edit_patient_disease_groups', methods=['GET', 'POST'])
def view_patient_disease_groups(patient_id):
    patient = Patient.query.get_or_404(patient_id)

    if not patient.can_view(current_user):
        abort(403)

    form = PatientDiseaseGroupForm()

    # TODO permissions
    # TODO sort order
    form.disease_group_id.choices = [(x.id, x.name) for x in DiseaseGroup.query.all() if not patient.in_disease_group(x)]

    if request.method == 'POST':
        if not patient.can_edit(current_user):
            abort(403)

        if form.validate():
            disease_group_id = form.disease_group_id.data
            disease_group = DiseaseGroup.query.get_or_404(disease_group_id)
            add_patient_to_disease_group(patient, disease_group)
            db.session.commit()

            return redirect(url_for('patients.view_patient_disease_groups', patient_id=patient.id))

    context = dict(
        patient=patient,
        patient_data=get_patient_data(patient),
        form=form,
    )

    return render_template('patient/disease_groups.html', **context)


@bp.route('/<int:patient_id>/units/', endpoint='view_patient_units')
@bp.route('/<int:patient_id>/units/', endpoint='edit_patient_units', methods=['GET', 'POST'])
def view_patient_units(patient_id):
    patient = Patient.query.get_or_404(patient_id)

    if not patient.can_view(current_user):
        abort(403)

    form = PatientUnitForm()

    # TODO permissions
    # TODO sort order
    form.unit_id.choices = [(x.id, x.name) for x in Unit.query.all() if not patient.in_unit(x)]

    if request.method == 'POST':
        if not patient.can_edit(current_user):
            abort(403)

        if form.validate():
            unit_id = form.unit_id.data
            unit = Unit.query.get_or_404(unit_id)
            add_patient_to_unit(patient, unit)
            db.session.commit()

            return redirect(url_for('patients.view_patient_units', patient_id=patient.id))

    context = dict(
        patient=patient,
        patient_data=get_patient_data(patient),
        form=form,
    )

    return render_template('patient/units.html', **context)


RECRUIT_PATIENT_SEARCH = 1
RECRUIT_PATIENT_RADAR = 2
RECRUIT_PATIENT_RDC = 3
RECRUIT_PATIENT_NEW = 4
RECRUIT_PATIENT_ADDED = 5
RECRUIT_PATIENT_FIRST_STEP = RECRUIT_PATIENT_SEARCH
RECRUIT_PATIENT_STEPS = [
    RECRUIT_PATIENT_SEARCH,
    RECRUIT_PATIENT_RADAR,
    RECRUIT_PATIENT_RDC,
    RECRUIT_PATIENT_NEW,
    RECRUIT_PATIENT_ADDED,
]


def set_recruit_patient_step(step):
    session['recruit_patient_step'] = step


def redirect_to_recruit_patient_step(step):
    set_recruit_patient_step(step)
    return redirect(url_for('patients.recruit_patient'))


@bp.route('/recruit/', methods=['GET', 'POST'])
def recruit_patient():
    if not current_user.has_recruit_patient_permission:
        abort(403)

    # Go back to the first step
    if 'restart' in request.form:
        return redirect_to_recruit_patient_step(RECRUIT_PATIENT_FIRST_STEP)

    step = session.get('recruit_patient_step')

    # First load
    if step not in RECRUIT_PATIENT_STEPS:
        step = RECRUIT_PATIENT_FIRST_STEP

    # Handle user going back to patient search
    if 'recruit_patient_search' in request.form:
        step = RECRUIT_PATIENT_SEARCH

    # Handle user going back to list of RaDaR patients
    if 'recruit_patient_radar' in request.form:
        if step in [RECRUIT_PATIENT_RADAR, RECRUIT_PATIENT_RDC, RECRUIT_PATIENT_NEW]:
            step = RECRUIT_PATIENT_RADAR
        else:
            return redirect_to_recruit_patient_step(RECRUIT_PATIENT_FIRST_STEP)

    # Handle user going back to list of RDC patients
    if 'recruit_patient_rdc' in request.form:
        if step in [RECRUIT_PATIENT_RDC, RECRUIT_PATIENT_NEW]:
            step = RECRUIT_PATIENT_RDC
        else:
            return redirect_to_recruit_patient_step(RECRUIT_PATIENT_FIRST_STEP)

    if step == RECRUIT_PATIENT_SEARCH:
        return recruit_patient_search_step()
    elif step == RECRUIT_PATIENT_RADAR:
        return recruit_patient_radar_step()
    elif step == RECRUIT_PATIENT_RDC:
        return recruit_patient_rdc_step()
    elif step == RECRUIT_PATIENT_NEW:
        return recruit_patient_new_step()
    elif step == RECRUIT_PATIENT_ADDED:
        return recruit_patient_added_step()


def recruit_patient_search_step():
    form = RecruitPatientSearchForm()

    # TODO permissions
    # TODO order
    form.unit_id.choices = [(x.id, x.name) for x in Unit.query.all()]
    form.disease_group_id.choices = [(x.id, x.name) for x in DiseaseGroup.query.all()]

    if form.validate_on_submit():
        unit_id = form.unit_id.data
        disease_group_id = form.disease_group_id.data
        date_of_birth = form.date_of_birth.data
        first_name = form.first_name.data
        last_name = form.last_name.data
        nhs_no = form.nhs_no.data
        chi_no = form.chi_no.data

        session['recruit_patient_unit_id'] = unit_id
        session['recruit_patient_disease_group_id'] = disease_group_id
        session['recruit_patient_date_of_birth'] = date_of_birth.strftime('%Y-%m-%d')
        session['recruit_patient_first_name'] = first_name
        session['recruit_patient_last_name'] = last_name
        session['recruit_patient_nhs_no'] = nhs_no
        session['recruit_patient_chi_no'] = chi_no

        radar_patients = find_existing_radar_patients(date_of_birth, first_name, last_name, nhs_no, chi_no)

        # Found potential RaDaR matched
        if radar_patients:
            return redirect_to_recruit_patient_step(RECRUIT_PATIENT_RADAR)

        rdc_patients = find_existing_rdc_patients(date_of_birth, first_name, last_name, nhs_no, chi_no)

        # Found potential RDC matches
        if rdc_patients:
            return redirect_to_recruit_patient_step(RECRUIT_PATIENT_RDC)

        # No matches found, make a new patient
        return redirect_to_recruit_patient_step(RECRUIT_PATIENT_NEW)

    context = dict(
        form=form
    )

    return render_template('recruit_patient/search.html', **context)


def recruit_patient_radar_step():
    try:
        date_of_birth = datetime.strptime(session['recruit_patient_date_of_birth'], '%Y-%m-%d')
        first_name = session['recruit_patient_first_name']
        last_name = session['recruit_patient_last_name']
        nhs_no = session['recruit_patient_nhs_no']
        chi_no = session['recruit_patient_chi_no']
    except (ValueError, KeyError):
        return redirect_to_recruit_patient_step(RECRUIT_PATIENT_FIRST_STEP)

    patients = find_existing_radar_patients(date_of_birth, first_name, last_name, nhs_no, chi_no)

    # No matching RaDaR patients found
    if not patients:
        rdc_patients = find_existing_rdc_patients(date_of_birth, first_name, last_name, nhs_no, chi_no)

        # Potential match found in RDC
        if rdc_patients:
            step = RECRUIT_PATIENT_RDC
        else:
            step = RECRUIT_PATIENT_NEW

        return redirect_to_recruit_patient_step(step)

    form = RecruitPatientRadarForm()
    form.patient_id.choices = [(x.id, x.id) for x in patients]

    if form.validate_on_submit():
        patient_id = form.patient_id.data

        # User chose one of the existing RaDaR patients
        if patient_id is not None:
            patient = None

            # Get the patient with this id
            for x in patients:
                if x.id == patient_id:
                    patient = x

            if patient is not None:
                try:
                    unit_id = session['recruit_patient_unit_id']
                    disease_group_id = session['recruit_patient_disease_group_id']
                except KeyError:
                    return redirect_to_recruit_patient_step(RECRUIT_PATIENT_FIRST_STEP)

                unit = Unit.query.get(unit_id)
                disease_group = DiseaseGroup.query.get(disease_group_id)

                if unit is None or disease_group is None:
                    return redirect_to_recruit_patient_step(RECRUIT_PATIENT_FIRST_STEP)

                session['recruit_patient_patient_id'] = patient_id
                return redirect_to_recruit_patient_step(RECRUIT_PATIENT_ADDED)
        else:
            rdc_patients = find_existing_rdc_patients(date_of_birth, first_name, last_name, nhs_no, chi_no)

            if rdc_patients:
                step = RECRUIT_PATIENT_RDC
            else:
                step = RECRUIT_PATIENT_NEW

            return redirect_to_recruit_patient_step(step)

    context = dict(
        patients=patients,
        form=form
    )

    return render_template('recruit_patient/radar.html', **context)


def recruit_patient_rdc_step():
    try:
        date_of_birth = datetime.strptime(session['recruit_patient_date_of_birth'], '%Y-%m-%d')
        first_name = session['recruit_patient_first_name']
        last_name = session['recruit_patient_last_name']
        nhs_no = session['recruit_patient_nhs_no']
        chi_no = session['recruit_patient_chi_no']
    except (ValueError, KeyError):
        return redirect_to_recruit_patient_step(RECRUIT_PATIENT_FIRST_STEP)

    patients = find_existing_rdc_patients(date_of_birth, first_name, last_name, nhs_no, chi_no)

    if patients:
        form = RecruitPatientRdcForm()

        if form.validate_on_submit():
            mpiid = form.mpiid.data

            # User chose one of the matches
            if mpiid is not None:
                # Check MPIID is still valid
                if mpiid in [x['mpiid'] for x in patients]:
                    # TODO
                    patient = Patient()
                    db.session.add(patient)
                    db.session.commit()

                    session['recruit_patient_patient_id'] = patient.id
                    return redirect_to_recruit_patient_step(RECRUIT_PATIENT_ADDED)
            else:
                # User rejected all of the candidates, make a new patient
                return redirect_to_recruit_patient_step(RECRUIT_PATIENT_NEW)
    else:
        # No matches found in the RDC
        return redirect_to_recruit_patient_step(RECRUIT_PATIENT_NEW)

    context = dict(
        patients=patients,
        form=form,
    )

    return render_template('recruit_patient/rdc.html', **context)


def recruit_patient_new_step():
    try:
        unit_id = session['recruit_patient_unit_id']
        disease_group_id = session['recruit_patient_disease_group_id']
        date_of_birth = datetime.strptime(session['recruit_patient_date_of_birth'], '%Y-%m-%d')
        first_name = session['recruit_patient_first_name']
        last_name = session['recruit_patient_last_name']
        nhs_no = session['recruit_patient_nhs_no']
        chi_no = session['recruit_patient_chi_no']
    except (ValueError, KeyError):
        return redirect_to_recruit_patient_step(RECRUIT_PATIENT_FIRST_STEP)

    unit = Unit.query.get(unit_id)
    disease_group = DiseaseGroup.query.get(disease_group_id)

    if unit is None or disease_group is None:
        return redirect_to_recruit_patient_step(RECRUIT_PATIENT_FIRST_STEP)

    form = DemographicsForm(
        date_of_birth=date_of_birth,
        first_name=first_name,
        last_name=last_name,
        nhs_no=nhs_no,
        chi_no=chi_no
    )

    if form.validate_on_submit():
        date_of_birth = form.date_of_birth.data
        first_name = form.first_name.data
        last_name = form.last_name.data
        nhs_no = form.nhs_no.data
        chi_no = form.chi_no.data

        session['recruit_patient_date_of_birth'] = date_of_birth.strftime('%Y-%m-%d')
        session['recruit_patient_first_name'] = first_name
        session['recruit_patient_first_name'] = last_name
        session['recruit_patient_nhs_no'] = nhs_no
        session['recruit_patient_chi_no'] = chi_no

        # TODO fresh check against RaDaR and RDC

        # Create new patient
        patient = Patient()
        patient.registered_user = current_user
        db.session.add(patient)

        # Save demographics
        demographics = Demographics(patient=patient)
        form.populate_obj(demographics)
        save_radar_demographics(demographics)
        db.session.add(demographics)

        # Add to groups
        add_patient_to_unit(patient, unit)
        add_patient_to_disease_group(patient, disease_group)

        db.session.commit()

        session['recruit_patient_patient_id'] = patient.id
        return redirect_to_recruit_patient_step(RECRUIT_PATIENT_ADDED)

    context = dict(
        form=form
    )

    return render_template('recruit_patient/new.html', **context)


def recruit_patient_added_step():
    try:
        patient_id = session['recruit_patient_patient_id']
    except KeyError:
        return redirect_to_recruit_patient_step(RECRUIT_PATIENT_FIRST_STEP)

    patient = Patient.query.get(patient_id)

    # Check patient still exists
    if patient is None:
        flash('Patient has been deleted.', 'error')
        return redirect_to_recruit_patient_step(RECRUIT_PATIENT_FIRST_STEP)

    # User might not be able to view this patient (anymore)
    if not patient.can_view(current_user):
        flash('Patient added successfully.', 'success')
        return redirect_to_recruit_patient_step(RECRUIT_PATIENT_FIRST_STEP)

    context = dict(
        patient=patient
    )

    set_recruit_patient_step(RECRUIT_PATIENT_FIRST_STEP)
    return render_template('recruit_patient/added.html', **context)


def save_radar_demographics(demographics):
    sda_bundle = demographics_to_sda_bundle(demographics)
    sda_bundle.serialize()
    demographics.sda_bundle = sda_bundle


def add_patient_to_unit(patient, unit):
    unit_patient = UnitPatient()
    unit_patient.created_user = current_user
    unit_patient.patient = patient
    unit_patient.unit = unit

    # TODO permissions

    db.session.add(unit_patient)


def add_patient_to_disease_group(patient, disease_group):
    disease_group_patient = DiseaseGroupPatient()
    disease_group_patient.created_user = current_user
    disease_group_patient.patient = patient
    disease_group_patient.disease_group = disease_group

    # TODO permissions

    db.session.add(disease_group_patient)