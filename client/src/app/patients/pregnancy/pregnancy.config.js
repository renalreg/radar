(function() {
  'use strict';

  var app = angular.module('radar.patients.pregnancy');

  app.config(['$stateProvider', function($stateProvider) {
    $stateProvider.state('patient.pregnancy', {
      url: '/pregnancy',
      templateUrl: 'app/patients/pregnancy/pregnancy.html'
    });
  }]);
})();
