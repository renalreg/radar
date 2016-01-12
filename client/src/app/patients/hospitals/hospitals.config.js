(function() {
  'use strict';

  var app = angular.module('radar.patients.hospitals');

  app.config(['$stateProvider', function($stateProvider) {
    $stateProvider.state('patient.hospitals', {
      url: '/hospitals',
      templateUrl: 'app/patients/hospitals/hospitals.html'
    });
  }]);
})();
