(function() {
  'use strict';

  var app = angular.module('radar.dialysis');

  app.config(function($stateProvider) {
    $stateProvider.state('patient.dialysis', {
      url: '/dialysis',
      templateUrl: 'app/dialysis/dialysis-list.html',
      controller: 'DialysisListController',
      resolve: {
        items: function(patient, DialysisService) {
          return DialysisService.getList(patient.id);
        }
      }
    });
  });
})();
