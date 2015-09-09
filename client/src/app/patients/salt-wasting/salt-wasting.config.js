(function() {
  'use strict';

  var app = angular.module('radar.patients.saltWasting');

  app.config(function($stateProvider) {
    $stateProvider.state('patient.saltWastingClinicalFeatures', {
      url: '/salt-wasting-clinical-features',
      templateUrl: 'app/patients/salt-wasting/clinical-features.html'
    });
  });
})();
