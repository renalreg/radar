(function() {
  'use strict';

  var app = angular.module('radar.patients.addresses');

  app.config(['$stateProvider', function($stateProvider) {
    $stateProvider.state('patient.addresses', {
      url: '/addresses',
      templateUrl: 'app/patients/addresses/addresses.html'
    });
  }]);
})();
