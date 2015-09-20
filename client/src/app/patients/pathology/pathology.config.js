(function() {
  'use strict';

  var app = angular.module('radar.patients.pathology');

  app.config(['$stateProvider', function($stateProvider) {
    $stateProvider.state('patient.pathology', {
      url: '/pathology',
      templateUrl: 'app/patients/pathology/pathology.html'
    });
  }]);
})();
