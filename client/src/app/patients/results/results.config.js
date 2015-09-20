(function() {
  'use strict';

  var app = angular.module('radar.patients.results');

  app.config(function($stateProvider) {
    $stateProvider.state('patient.results', {
      url: '/results',
      templateUrl: 'app/patients/results/results.html'
    });
  });
})();
