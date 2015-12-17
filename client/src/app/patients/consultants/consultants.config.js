(function() {
  'use strict';

  var app = angular.module('radar.patients.consultants');

  app.config(['$stateProvider', function($stateProvider) {
    $stateProvider.state('patient.consultants', {
      url: '/consultants',
      templateUrl: 'app/patients/consultants/consultants.html'
    });
  }]);
})();
