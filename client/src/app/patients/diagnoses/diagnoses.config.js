(function() {
  'use strict';

  var app = angular.module('radar.patients.diagnoses');

  app.config(['$stateProvider', function($stateProvider) {
    $stateProvider.state('patient.diagnoses', {
      url: '/diagnoses',
      templateUrl: 'app/patients/diagnoses/diagnoses.html'
    });
  }]);
})();
