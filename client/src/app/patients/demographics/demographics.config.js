(function() {
  'use strict';

  var app = angular.module('radar.patients.demographics');

  app.config(function($stateProvider) {
    $stateProvider.state('patient.demographics', {
      url: '',
      templateUrl: 'app/patients/demographics/demographics.html'
    });

    $stateProvider.state('patient.addresses', {
      url: '/addresses',
      templateUrl: 'app/patients/demographics/addresses.html'
    });

    $stateProvider.state('patient.aliases', {
      url: '/aliases',
      templateUrl: 'app/patients/demographics/aliases.html'
    });

    $stateProvider.state('patient.numbers', {
      url: '/numbers',
      templateUrl: 'app/patients/demographics/numbers.html'
    });
  });
})();
