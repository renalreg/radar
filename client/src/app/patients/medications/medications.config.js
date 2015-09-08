(function() {
  'use strict';

  var app = angular.module('radar.patients.medications');

  app.config(function($stateProvider) {
    $stateProvider.state('patient.medications', {
      url: '/medications',
      templateUrl: 'app/patients/medications/medications.html'
    });
  });
})();
