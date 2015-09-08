(function() {
  'use strict';

  var app = angular.module('radar.patients.units');

  app.config(function($stateProvider) {
    $stateProvider.state('patient.units', {
      url: '/units',
      templateUrl: 'app/patients/units/unit-list.html'
    });
  });
})();
