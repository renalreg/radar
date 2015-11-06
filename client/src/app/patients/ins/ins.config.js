(function() {
  'use strict';

  var app = angular.module('radar.patients.ins');

  app.config(['$stateProvider', function($stateProvider) {
    $stateProvider.state('patient.insClinicalFeatures', {
      url: '/ins-clinical-features',
      templateUrl: 'app/patients/ins/clinical-features.html'
    });
  }]);
})();
