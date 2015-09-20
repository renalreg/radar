(function() {
  'use strict';

  var app = angular.module('radar.patients.results');

  app.config(['$stateProvider', function($stateProvider) {
    $stateProvider.state('patient.results', {
      url: '/results',
      abstract: true,
      templateUrl: 'app/patients/results/results.html'
    });

    $stateProvider.state('patient.results.list', {
      url: '',
      templateUrl: 'app/patients/results/result-list.html'
    });

    $stateProvider.state('patient.results.graphs', {
      url: '/graphs',
      templateUrl: 'app/patients/results/result-graphs.html'
    });
  }]);
})();
