(function() {
  'use strict';

  var app = angular.module('radar.patients.nephrectomies');

  app.config(['$stateProvider', function($stateProvider) {
    $stateProvider.state('patient.nephrectomies', {
      url: '/nephrectomies',
      templateUrl: 'app/patients/nephrectomies/nephrectomies.html'
    });
  }]);
})();
