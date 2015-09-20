(function() {
  'use strict';

  var app = angular.module('radar.patients.demographics');

  app.config(['$stateProvider', function($stateProvider) {
    $stateProvider.state('patient.demographics', {
      url: '',
      templateUrl: 'app/patients/demographics/demographics.html'
    });
  }]);
})();
