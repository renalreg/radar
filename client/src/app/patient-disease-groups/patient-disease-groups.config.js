(function() {
  'use strict';

  var app = angular.module('radar.patientDiseaseGroups');

  app.config(function($stateProvider) {
    $stateProvider.state('patient.diseaseGroups', {
      url: '/disease-groups',
      templateUrl: 'app/patient-disease-groups/patient-disease-group-list.html'
    });
  });
})();
