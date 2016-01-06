(function() {
  'use strict';

  var app = angular.module('radar.patients.metadata');

  app.config(['$stateProvider', function($stateProvider) {
    $stateProvider.state('patient.metadata', {
      url: '/metadata',
      templateUrl: 'app/patients/metadata/metadata.html'
    });
  }]);
})();
