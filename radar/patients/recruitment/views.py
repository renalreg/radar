from datetime import datetime

from flask import render_template, abort, request, url_for, redirect, session, flash, Blueprint
from flask_login import current_user

from radar.database import db
from radar.disease_groups.models import DiseaseGroup
from radar.patients.models import Patient, Demographics
from radar.patients.recruitment.forms import RecruitPatientSearchForm, RecruitPatientRadarForm, RecruitPatientRDCForm
from radar.patients.forms import DemographicsForm
from radar.patients.recruitment.services import find_existing_radar_patients, find_existing_rdc_patients
from radar.patients.views import save_radar_demographics, add_patient_to_unit, add_patient_to_disease_group
from radar.units.models import Unit


bp = Blueprint('recruitment', __name__)


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
    return redirect(url_for('recruitment.recruit_patient'))


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

    return render_template('recruitment/search.html', **context)


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

    return render_template('recruitment/radar.html', **context)


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
        form = RecruitPatientRDCForm()

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

    return render_template('recruitment/rdc.html', **context)


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
        patient.recruited_user = current_user
        patient.recruited_unit = unit
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

    return render_template('recruitment/new.html', **context)


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
    return render_template('recruitment/added.html', **context)