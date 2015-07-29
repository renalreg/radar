(function() {
  'use strict';

  var app = angular.module('radar.patient');

  app.config(function($stateProvider) {
    $stateProvider.state('patients', {
      url: '/patients',
      templateUrl: 'app/patient/patient-list.html',
      controller: 'PatientListController'
    });

    $stateProvider.state('patient', {
      url: '/patients/:patientId',
      abstract: true,
      templateUrl: 'app/patient/patient-detail.html',
      controller: 'PatientDetailController',
      resolve: {
        patient: function($stateParams, PatientService) {
          return PatientService.getPatient($stateParams.patientId);
        }
      }
    });
  });
})();
