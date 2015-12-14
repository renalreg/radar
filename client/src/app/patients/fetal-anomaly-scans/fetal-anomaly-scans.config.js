(function() {
  'use strict';

  var app = angular.module('radar.patients.fetalAnomalyScans');

  app.config(['$stateProvider', function($stateProvider) {
    $stateProvider.state('patient.fetalAnomalyScans', {
      url: '/fetal-anomaly-scans',
      templateUrl: 'app/patients/fetal-anomaly-scans/fetal-anomaly-scans.html'
    });
  }]);
})();
