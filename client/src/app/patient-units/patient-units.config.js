(function() {
  'use strict';

  var app = angular.module('radar.patientUnits');

  app.config(function($stateProvider) {
    $stateProvider.state('patient.units', {
      url: '/units',
      templateUrl: 'app/patient-units/unit-list.html'
    });
  });
})();
