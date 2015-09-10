(function() {
  'use strict';

  var app = angular.module('radar.patients.cohorts');

  app.config(function($stateProvider) {
    $stateProvider.state('patient.cohorts', {
      url: '/cohorts',
      templateUrl: 'app/patients/cohorts/cohorts.html'
    });
  });
})();
