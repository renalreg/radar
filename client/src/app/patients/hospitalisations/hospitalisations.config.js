(function() {
  'use strict';

  var app = angular.module('radar.patients.hospitalisations');

  app.config(['$stateProvider', function($stateProvider) {
    $stateProvider.state('patient.hospitalisations', {
      url: '/hospitalisations',
      templateUrl: 'app/patients/hospitalisations/hospitalisations.html'
    });
  }]);
})();

