(function() {
  'use strict';

  var app = angular.module('radar.patients.aliases');

  app.config(['$stateProvider', function($stateProvider) {
    $stateProvider.state('patient.aliases', {
      url: '/aliases',
      templateUrl: 'app/patients/aliases/aliases.html'
    });
  }]);
})();
