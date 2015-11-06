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

  // TODO refactor into state and cohort flag
  app.constant('patientFeatures', {
    ADDRESSES: {
      text: 'Addresses',
      state: 'patient.addresses({patientId: patient.id})'
    },
    ALIASES: {
      text: 'Aliases',
      state: 'patient.aliases({patientId: patient.id})'
    },
    DEMOGRAPHICS: {
      text: 'Demographics',
      state: 'patient.demographics({patientId: patient.id})'
    },
    DIAGNOSES: {
      text: 'Diagnoses',
      state: 'patient.diagnoses({patientId: patient.id, cohortId: cohort.id})'
    },
    DIALYSIS: {
      text: 'Dialysis',
      state: 'patient.dialysis({patientId: patient.id})'
    },
    COHORTS: {
      text: 'Cohorts',
      state: 'patient.cohorts({patientId: patient.id})'
    },
    COMORBIDITIES: {
      text: 'Comorbidities',
      state: 'patient.comorbidities({patientId: patient.id})'
    },
    FAMILY_HISTORY: {
      text: 'Family History',
      state: 'patient.familyHistory({patientId: patient.id, cohortId: cohort.id})'
    },
    GENETICS: {
      text: 'Genetics',
      state: 'patient.genetics({patientId: patient.id, cohortId: cohort.id})'
    },
    HOSPITALISATIONS: {
      text: 'Hospitalisations',
      state: 'patient.hospitalisations({patientId: patient.id})'
    },
    INS_CLINICAL_FEATURES: {
      text: 'Clinical Features',
      state: 'patient.insClinicalFeatures({patientId: patient.id})'
    },
    MEDICATIONS: {
      text: 'Medications',
      state: 'patient.medications({patientId: patient.id})'
    },
    META: {
      text: 'Meta',
      state: 'patient.meta({patientId: patient.id})'
    },
    NEPHRECTOMIES: {
      text: 'Nephrectomies',
      state: 'patients.nephrectomies({patientId: patient.id})'
    },
    NUMBERS: {
      text: 'Numbers',
      state: 'patient.numbers({patientId: patient.id})'
    },
    PATHOLOGY: {
      text: 'Pathology',
      state: 'patient.pathology({patientId: patient.id})'
    },
    PLASMAPHERESIS: {
      text: 'Plasmapheresis',
      state: 'patient.plasmapheresis({patientId: patient.id})'
    },
    RENAL_IMAGING: {
      text: 'Renal Imaging',
      state: 'patient.renalImaging({patientId: patient.id})'
    },
    RESULTS: {
      text: 'Results',
      state: 'patient.results.list({patientId: patient.id})'
    },
    SALT_WASTING_CLINICAL_FEATURES: {
      text: 'Clinical Features',
      state: 'patient.saltWastingClinicalFeatures({patientId: patient.id})'
    },
    TRANSPLANTS: {
      text: 'Transplants',
      state: 'patient.transplants({patientId: patient.id})'
    },
    UNITS: {
      text: 'Units',
      state: 'patient.units({patientId: patient.id})'
    }
  });

  app.constant('standardPatientFeatures', [
    'DEMOGRAPHICS',
    'RESULTS',
    'COMORBIDITIES',
    'PATHOLOGY',
    'MEDICATIONS',
    'DIALYSIS',
    'PLASMAPHERESIS',
    'TRANSPLANTS',
    'HOSPITALISATIONS',
    'COHORTS',
    'UNITS'
  ]);
})();
