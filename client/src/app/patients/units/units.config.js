(function() {
  'use strict';

  var app = angular.module('radar.patients.units');

  app.config(['$stateProvider', function($stateProvider) {
    $stateProvider.state('patient.units', {
      url: '/units',
      templateUrl: 'app/patients/units/units.html'
    });
  }]);
})();
