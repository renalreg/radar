(function() {
  'use strict';

  var app = angular.module('radar.patients');

  app.config(function($stateProvider) {
    $stateProvider.state('patients', {
      url: '/patients',
      templateUrl: 'app/patients/patient-list.html',
      controller: 'PatientListController',
      resolve: {
        patients: function(PatientService) {
          return PatientService.getPatients();
        }
      }
    });

    $stateProvider.state('patient', {
      url: '/patients/:patientId',
      abstract: true,
      templateUrl: 'app/patients/patient-detail.html',
      controller: 'PatientDetailController',
      resolve: {
        patient: function($stateParams, PatientService) {
          return PatientService.getPatient($stateParams.patientId);
        }
      }
    });
  });
})();
