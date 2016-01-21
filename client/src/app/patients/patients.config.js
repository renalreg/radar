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

  app.factory('patientPages', ['_', function(_) {
    function patientPage(name, state, cohort) {
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
      ADDRESSES: patientPage('Addresses', 'patient.addresses'),
      ALIASES: patientPage('Aliases', 'patient.aliases'),
      ALPORT_CLINICAL_PICTURES: patientPage('Clinical Pictures', 'patient.alportClinicalPictures'),
      DEMOGRAPHICS: patientPage('Demographics', 'patient.demographics'),
      DIAGNOSES: patientPage('Diagnoses', 'patient.diagnoses', true),
      DIALYSIS: patientPage('Dialysis', 'patient.dialysis'),
      COHORTS: patientPage('Cohorts', 'patient.cohorts'),
      CONSULTANTS: patientPage('Consultants', 'patient.consultants'),
      FAMILY_HISTORY: patientPage('Family History', 'patient.familyHistory', true),
      FETAL_ANOMALY_SCANS: patientPage('Fetal Anomaly Scans', 'patient.fetalAnomalyScans'),
      FETAL_ULTRASOUNDS: patientPage('Fetal Ultrasounds', 'patient.fetalUltrasounds'),
      GENETICS: patientPage('Genetics', 'patient.genetics', true),
      HNF1B_CLINICAL_PICTURES: patientPage('Clinical Pictures', 'patient.hnf1bClinicalPictures'),
      HOSPITALISATIONS: patientPage('Hospitalisations', 'patient.hospitalisations'),
      HOSPITALS: patientPage('Hospitals', 'patient.hospitals'),
      INS_CLINICAL_PICTURES: patientPage('Clinical Pictures', 'patient.insClinicalPictures'),
      INS_RELAPSES: patientPage('Relapses', 'patient.insRelapses'),
      MEDICATIONS: patientPage('Medications', 'patient.medications'),
      META: patientPage('Metadata', 'patient.metadata'),
      MPGN_CLINICAL_PICTURES: patientPage('Clinical Pictures', 'patient.mpgnClinicalPictures'),
      NEPHRECTOMIES: patientPage('Nephrectomies', 'patient.nephrectomies'),
      NUMBERS: patientPage('Numbers', 'patient.numbers'),
      PATHOLOGY: patientPage('Pathology', 'patient.pathology'),
      PLASMAPHERESIS: patientPage('Plasmapheresis', 'patient.plasmapheresis'),
      PREGNANCIES: patientPage('Pregnancies', 'patient.pregnancies'),
      PRIMARY_DIAGNOSIS: patientPage('Primary Diagnosis', 'patient.primaryDiagnosis'),
      RENAL_IMAGING: patientPage('Renal Imaging', 'patient.renalImaging'),
      RESULTS: patientPage('Results', 'patient.results'),
      SALT_WASTING_CLINICAL_FEATURES: patientPage('Clinical Features', 'patient.saltWastingClinicalFeatures'),
      TRANSPLANTS: patientPage('Transplants', 'patient.transplants')
    };
  }]);
})();
