from flask import render_template, flash, url_for, request, redirect
from flask.views import View
from radar.database import db_session
from radar.demographics.forms import DemographicsFormHandler
from radar.demographics.models import Demographics
from radar.models import SDAPatient, SDAContainer, Patient, Facility
from radar.patients.views import get_patient_detail_context


class DemographicsView(View):
    def dispatch_request(self, patient_id):
        context = get_patient_detail_context(patient_id)

        sda_patients = SDAPatient.query\
            .join(SDAContainer)\
            .join(Patient)\
            .filter(Patient.id == patient_id)\
            .all()

        demographics_list = []

        for sda_patient in sda_patients:
            demographics = dict()

            demographics['facility'] = sda_patient.sda_container.facility
            demographics['first_name'] = sda_patient.first_name
            demographics['last_name'] = sda_patient.last_name

            demographics_list.append(demographics)

        context['demographics_list'] = demographics_list

        return render_template('patient/demographics.html', **context)

class DemographicsEditView(View):
    methods = ['GET', 'POST']

    def dispatch_request(self, patient_id):
        context = get_patient_detail_context(patient_id)
        patient = context['patient']

        demographics = Demographics.query.filter(Demographics.patient == patient).first()

        if demographics is None:
            demographics = Demographics()
            demographics.patient = patient

        form = DemographicsFormHandler(demographics)
        context['form'] = form

        if request.method == 'POST':
            form.submit(request.form)

            if form.valid():
                # TODO

                sda_container = SDAContainer()
                sda_container.facility = Facility.query.get(1)
                sda_container.patient = patient

                sda_patient = SDAPatient()
                sda_patient.sda_container = sda_container
                sda_patient.first_name = demographics.first_name
                sda_patient.last_name = demographics.last_name

                demographics.sda_container = sda_container

                db_session.add(demographics)
                db_session.commit()

                flash('Demographics saved.', 'success')
                return redirect(url_for('demographics', patient_id=patient.id))

        return render_template('patient/demographics_edit.html', **context)