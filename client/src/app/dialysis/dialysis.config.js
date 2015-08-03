(function() {
  'use strict';

  var app = angular.module('radar.dialysis');

  app.config(function($stateProvider) {
    $stateProvider.state('patient.dialysis', {
      url: '/dialysis',
      templateUrl: 'app/dialysis/dialysis.html',
      controller: 'DialysisController'
    });
  });
})();
