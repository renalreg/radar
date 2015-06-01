from flask import render_template, Blueprint, abort, request, url_for, redirect, flash
from flask_login import current_user

from radar.lib.database import db
from radar.lib.facilities import get_radar_facility
from radar.lib.patients import get_facility_patients
from radar.models.disease_groups import DiseaseGroup
from radar.lib.forms.core import DeleteForm
from radar.models.patients import Patient, PatientDemographics
from radar.models.disease_groups import DiseaseGroupPatient
from radar.lib.ordering import Ordering
from radar.lib.pagination import paginate_query
from radar.lib.forms.patients import PatientSearchForm, PER_PAGE_DEFAULT, PER_PAGE_CHOICES, DemographicsForm, \
    PatientUnitForm, AddPatientDiseaseGroupForm, EditPatientDiseaseGroupForm
from radar.lib.demographics_sda import demographics_to_sda_bundle
from radar.lib.patient_search import PatientQueryBuilder
from radar.models.units import Unit, UnitPatient


bp = Blueprint('patients', __name__)


def get_patient_data(patient):
    units = sorted(patient.filter_units_for_user(current_user), key=lambda x: x.unit.name.lower())
    disease_groups = sorted(patient.filter_disease_groups_for_user(current_user), key=lambda x: x.disease_group.name.lower())

    return dict(
        units=units,
        disease_groups=disease_groups,
    )


def build_patient_search_query(user, form):
    builder = PatientQueryBuilder(user)

    if form.validate():
        include_inactive = form.include_inactive.data

        if form.first_name.data:
                builder.first_name(form.first_name.data)

        if form.last_name.data:
            builder.last_name(form.last_name.data)

        if form.unit_id.data:
            unit = Unit.query.get_or_404(form.unit_id.data)
            builder.unit(unit, include_inactive)

        if form.disease_group_id.data:
            disease_group = DiseaseGroup.query.get_or_404(form.disease_group_id.data)
            builder.disease_group(disease_group, include_inactive)

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

        if form.date_of_death.data:
            builder.date_of_death(form.date_of_death.data)

        if form.year_of_death.data:
            builder.year_of_death(form.year_of_death.data)

        if not include_inactive:
            builder.is_active(True)

        builder.order_by(form.order_by.data, form.order_direction.data)

    return builder.build()


@bp.route('/')
def view_patient_list():
    if not current_user.has_view_patient_permission:
        abort(403)

    form = PatientSearchForm(user=current_user, formdata=request.args, csrf_enabled=False)

    query = build_patient_search_query(current_user, form)

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
    )

    return render_template('patients.html', **context)


@bp.route('/<int:patient_id>/', endpoint='view_demographics_list')
@bp.route('/<int:patient_id>/', endpoint='view_patient')
def view_demographics_list(patient_id):
    patient = Patient.query.get_or_404(patient_id)

    if not patient.can_view(current_user):
        abort(403)

    facility_patients = get_facility_patients(patient)

    context = dict(
        patient=patient,
        patient_data=get_patient_data(patient),
        facility_patients=facility_patients
    )

    return render_template('patient/demographics.html', **context)


@bp.route('/<int:patient_id>/edit/', endpoint='edit_demographics', methods=['GET', 'POST'])
def edit_demographics(patient_id):
    facility = get_radar_facility()
    patient = Patient.query.get_or_404(patient_id)
    demographics = PatientDemographics.query\
        .filter(PatientDemographics.patient == patient)\
        .filter(PatientDemographics.facility == facility)\
        .first()

    if demographics is None:
        demographics = PatientDemographics(patient=patient, facility=facility)

    if not demographics.can_edit(current_user):
        abort(403)

    form = DemographicsForm(obj=demographics)

    if request.method == 'POST':
        if form.validate():
            form.populate_obj(demographics)
            db.session.add(demographics)
            db.session.commit()
            return redirect(url_for('patients.view_demographics_list', patient_id=demographics.patient.id))

    context = dict(
        patient=demographics.patient,
        patient_data=get_patient_data(demographics.patient),
        demographics=demographics,
        form=form,
    )

    return render_template('patient/edit_demographics.html', **context)


@bp.route('/<int:patient_id>/disease-groups/', endpoint='view_patient_disease_groups')
@bp.route('/<int:patient_id>/disease-groups/', endpoint='add_patient_disease_group', methods=['GET', 'POST'])
@bp.route('/<int:patient_id>/disease-groups/<int:disease_group_id>/', endpoint='edit_patient_disease_group', methods=['GET', 'POST'])
def view_patient_disease_groups(patient_id, disease_group_id=None):
    patient = Patient.query.get_or_404(patient_id)

    if not patient.can_view(current_user):
        abort(403)

    disease_group = None

    if disease_group_id is None:
        form = AddPatientDiseaseGroupForm()

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
                flash('Saved.', 'success')
                return redirect(url_for('patients.view_patient_disease_groups', patient_id=patient.id))
    else:
        disease_group = DiseaseGroupPatient.query\
            .filter(DiseaseGroupPatient.patient == patient)\
            .filter(DiseaseGroupPatient.id == disease_group_id)\
            .first_or_404()

        if not disease_group.can_edit(disease_group):
            abort(403)

        form = EditPatientDiseaseGroupForm(obj=disease_group)

        if form.validate_on_submit():
            disease_group.is_active = form.is_active.data
            db.session.commit()
            flash('Saved.', 'success')
            return redirect(url_for('patients.view_patient_disease_groups', patient_id=patient.id))

    context = dict(
        patient=patient,
        patient_data=get_patient_data(patient),
        form=form,
        disease_group=disease_group,
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


@bp.route('/<int:patient_id>/delete/', methods=['GET', 'POST'])
def delete_patient(patient_id):
    patient = Patient.query.get_or_404(patient_id)

    # TODO probably shouldn't be able to delete a patient who belongs to non-editable units

    if not patient.can_edit(current_user):
        abort(403)

    form = DeleteForm()

    if form.validate_on_submit():
        db.session.delete(patient)
        db.session.commit()
        flash('Patient deleted.', 'success')
        return redirect(url_for('patients.view_patient_list'))
    else:
        context = dict(
            patient=patient,
            patient_data=get_patient_data(patient)
        )

        return render_template('patient/delete.html', **context)


def save_radar_demographics(demographics):
    sda_bundle = demographics_to_sda_bundle(demographics)
    sda_bundle.serialize()
    demographics.sda_bundle = sda_bundle


def add_patient_to_unit(patient, unit):
    unit_patient = UnitPatient()
    unit_patient.patient = patient
    unit_patient.unit = unit

    # TODO permissions

    db.session.add(unit_patient)


def add_patient_to_disease_group(patient, disease_group):
    disease_group_patient = DiseaseGroupPatient()
    disease_group_patient.patient = patient
    disease_group_patient.disease_group = disease_group

    # TODO permissions

    db.session.add(disease_group_patient)