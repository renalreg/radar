(function() {
  'use strict';

  var app = angular.module('radar.patients.diseaseGroups');

  app.config(function($stateProvider) {
    $stateProvider.state('patient.diseaseGroups', {
      url: '/disease-groups',
      templateUrl: 'app/patients/disease-groups/patient-disease-group-list.html'
    });
  });
})();
