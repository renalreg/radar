(function() {
  'use strict';

  var app = angular.module('radar.units');

  app.config(function($stateProvider) {
    $stateProvider.state('units', {
      url: '/units',
      templateUrl: 'app/units/unit-list.html'
    });

    $stateProvider.state('unit', {
      url: '/units/:unitId',
      templateUrl: 'app/units/unit-detail.html'
    });
  });
})();
