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

  function patient_feature(name, state, cohort) {
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

  app.constant('patientFeatures', {
    ADDRESSES: patient_feature('Addresses', 'patient.addresses'),
    ALIASES: patient_feature('Aliases', 'patient.aliases'),
    DEMOGRAPHICS: patient_feature('Demographics', 'patient.demographics'),
    DIAGNOSES: patient_feature('Diagnoses', 'patient.diagnoses', true),
    DIALYSIS: patient_feature('Dialysis', 'patient.dialysis'),
    COHORTS: patient_feature('Cohorts', 'patient.cohorts'),
    COMORBIDITIES: patient_feature('Comorbidities', 'patient.comorbidities'),
    FAMILY_HISTORY: patient_feature('Family History', 'patient.familyHistory', true),
    GENETICS: patient_feature('Genetics', 'patient.genetics', true),
    HOSPITALISATIONS: patient_feature('Hospitalisations', 'patient.hospitalisations'),
    INS_CLINICAL_PICTURES: patient_feature('Clinical Pictures', 'patient.insClinicalPictures'),
    INS_RELAPSES: patient_feature('Relapses', 'patient.insRelapses'),
    MEDICATIONS: patient_feature('Medications', 'patient.medications'),
    META: patient_feature('Meta', 'patient.meta'),
    NEPHRECTOMIES: patient_feature('Nephrectomies', 'patient.nephrectomies'),
    NUMBERS: patient_feature('Numbers', 'patient.numbers'),
    PATHOLOGY: patient_feature('Pathology', 'patient.pathology'),
    PLASMAPHERESIS: patient_feature('Plasmapheresis', 'patient.plasmapheresis'),
    RENAL_IMAGING: patient_feature('Renal Imaging', 'patient.renalImaging'),
    RESULTS: patient_feature('Results', 'patient.results.table'),
    SALT_WASTING_CLINICAL_FEATURES: patient_feature('Clinical Features', 'patient.saltWastingClinicalFeatures'),
    TRANSPLANTS: patient_feature('Transplants', 'patient.transplants'),
    UNITS: patient_feature('Units', 'patient.units')
  });
})();
