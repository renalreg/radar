(function() {
  'use strict';

  var app = angular.module('radar.patients.pregnancies');

  app.config(['$stateProvider', function($stateProvider) {
    $stateProvider.state('patient.pregnancies', {
      url: '/pregnancies',
      templateUrl: 'app/patients/pregnancies/pregnancies.html'
    });
  }]);
})();
