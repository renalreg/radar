(function() {
  'use strict';

  var app = angular.module('radar.patients.fetalUltrasounds');

  app.config(['$stateProvider', function($stateProvider) {
    $stateProvider.state('patient.fetalUltrasounds', {
      url: '/fetal-ultrasounds',
      templateUrl: 'app/patients/fetal-ultrasounds/fetal-ultrasounds.html'
    });
  }]);
})();
