(function() {
  'use strict';

  var app = angular.module('radar.patients.demographics');

  app.config(function($stateProvider) {
    $stateProvider.state('patient.demographics', {
      url: '',
      templateUrl: 'app/patients/demographics/demographics-list.html'
    });
  });
})();
