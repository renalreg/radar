(function() {
  'use strict';

  var app = angular.module('radar.patients.familyHistory');

  app.config(function($stateProvider) {
    $stateProvider.state('patient.familyHistory', {
      url: '/family-history',
      templateUrl: 'app/patients/family-history/family-history.html'
    });
  });
})();

