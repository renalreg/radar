(function() {
  'use strict';

  var app = angular.module('radar.patients.numbers');

  app.config(function($stateProvider) {
    $stateProvider.state('patient.numbers', {
      url: '/numbers',
      templateUrl: 'app/patients/numbers/numbers.html'
    });
  });
})();
