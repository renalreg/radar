(function() {
  'use strict';

  var app = angular.module('radar.units');

  app.config(function($stateProvider) {
    $stateProvider.state('patient.units', {
      url: '/units',
      templateUrl: 'app/units/unit-list.html',
      controller: 'UnitListController'
    });
  });
})();
