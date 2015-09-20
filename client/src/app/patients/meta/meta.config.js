(function() {
  'use strict';

  var app = angular.module('radar.patients.meta');

  app.config(['$stateProvider', function($stateProvider) {
    $stateProvider.state('patient.meta', {
      url: '/meta',
      templateUrl: 'app/patients/meta/meta.html'
    });
  }]);
})();
