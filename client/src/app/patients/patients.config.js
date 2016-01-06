(function() {
  'use strict';

  var app = angular.module('radar.patients');

  app.config(['$stateProvider', function($stateProvider) {
    $stateProvider.state('patients', {
      url: '/patients',
      templateUrl: 'app/patients/patient-list.html',
      controller: ['$scope', '$controller', 'PatientListController', function($scope, $controller, PatientListController) {
        $controller(PatientListController, {$scope: $scope});
      }]
    });

    $stateProvider.state('patient', {
      url: '/patients/:patientId',
      abstract: true,
      templateUrl: 'app/patients/patient-detail.html',
      controller: 'PatientDetailController',
      resolve: {
        patient: ['$stateParams', 'store', function($stateParams, store) {
          return store.findOne('patients', $stateParams.patientId);
        }]
      }
    });

    $stateProvider.state('patient.all', {
      url: '/all',
      templateUrl: 'app/patients/all.html'
    });
  }]);

  app.factory('patientFeatures', ['_', function(_) {
    function patientFeature(name, state, cohort) {
      if (cohort === undefined) {
        cohort = false;
      }

      var stateParams = {
        patientId: 'patient.id'
      };

      if (cohort) {
        stateParams.cohortId = 'cohort.id';
      }

      state = state + '({' + _.map(stateParams, function(v, k) {
        return k + ': ' + v;
      }).join(', ') + '})';

      return {
        name: name,
        state: state
      };
    }

    return {
      ADDRESSES: patientFeature('Addresses', 'patient.addresses'),
      ALIASES: patientFeature('Aliases', 'patient.aliases'),
      ALPORT_CLINICAL_PICTURES: patientFeature('Clinical Pictures', 'patient.alportClinicalPictures'),
      DEMOGRAPHICS: patientFeature('Demographics', 'patient.demographics'),
      DIAGNOSES: patientFeature('Diagnosis', 'patient.diagnoses', true),
      DIALYSIS: patientFeature('Dialysis', 'patient.dialysis'),
      COHORTS: patientFeature('Cohorts', 'patient.cohorts'),
      COMORBIDITIES: patientFeature('Comorbidities', 'patient.comorbidities'),
      CONSULTANTS: patientFeature('Consultants', 'patient.consultants'),
      FAMILY_HISTORY: patientFeature('Family History', 'patient.familyHistory', true),
      FETAL_ANOMALY_SCANS: patientFeature('Fetal Anomaly Scans', 'patient.fetalAnomalyScans'),
      FETAL_ULTRASOUNDS: patientFeature('Fetal Ultrasounds', 'patient.fetalUltrasounds'),
      GENETICS: patientFeature('Genetics', 'patient.genetics', true),
      HNF1B_CLINICAL_PICTURES: patientFeature('Clinical Pictures', 'patient.hnf1bClinicalPictures'),
      HOSPITALISATIONS: patientFeature('Hospitalisations', 'patient.hospitalisations'),
      INS_CLINICAL_PICTURES: patientFeature('Clinical Pictures', 'patient.insClinicalPictures'),
      INS_RELAPSES: patientFeature('Relapses', 'patient.insRelapses'),
      MEDICATIONS: patientFeature('Medications', 'patient.medications'),
      META: patientFeature('Meta', 'patient.meta'),
      MPGN_CLINICAL_PICTURES: patientFeature('Clinical Pictures', 'patient.mpgnClinicalPictures'),
      NEPHRECTOMIES: patientFeature('Nephrectomies', 'patient.nephrectomies'),
      NUMBERS: patientFeature('Numbers', 'patient.numbers'),
      PATHOLOGY: patientFeature('Pathology', 'patient.pathology'),
      PLASMAPHERESIS: patientFeature('Plasmapheresis', 'patient.plasmapheresis'),
      PREGNANCIES: patientFeature('Pregnancies', 'patient.pregnancies'),
      RENAL_IMAGING: patientFeature('Renal Imaging', 'patient.renalImaging'),
      RESULTS: patientFeature('Results', 'patient.results.table'),
      SALT_WASTING_CLINICAL_FEATURES: patientFeature('Clinical Features', 'patient.saltWastingClinicalFeatures'),
      TRANSPLANTS: patientFeature('Transplants', 'patient.transplants'),
      UNITS: patientFeature('Units', 'patient.units')
    };
  }]);
})();
