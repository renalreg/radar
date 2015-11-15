(function() {
  'use strict';

  var app = angular.module('radar.recruitPatient');

  app.config(['$stateProvider', function($stateProvider) {
    $stateProvider.state('recruitPatient', {
      url: '/recruit-patient',
      abstract: true,
      controller: 'RecruitPatientController',
      templateUrl: 'app/recruit-patient/recruit-patient.html'
    });

    $stateProvider.state('recruitPatient.search', {
      url: '',
      templateUrl: 'app/recruit-patient/recruit-patient-search.html'
    });

    $stateProvider.state('recruitPatient.results', {
      url: '',
      templateUrl: 'app/recruit-patient/recruit-patient-results.html'
    });

    $stateProvider.state('recruitPatient.form', {
      url: '',
      templateUrl: 'app/recruit-patient/recruit-patient-form.html'
    });
  }]);
})();
