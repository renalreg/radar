(function() {
  'use strict';

  var app = angular.module('radar.patients.transplants');

  app.config(function($stateProvider) {
    $stateProvider.state('patient.transplants', {
      url: '/transplants',
      templateUrl: 'app/patients/transplants/transplants.html'
    });
  });
})();
