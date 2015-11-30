(function() {
  'use strict';

  var app = angular.module('radar.units');

  app.config(['$stateProvider', function($stateProvider) {
    $stateProvider.state('units', {
      url: '/units',
      templateUrl: 'app/units/unit-list.html',
      controller: 'UnitListController'
    });

    $stateProvider.state('unit', {
      url: '/units/:unitId',
      templateUrl: 'app/units/unit-detail.html',
      controller: 'UnitDetailController',
      resolve: {
        unit: ['$stateParams', 'store', function($stateParams, store) {
          return store.findOne('organisations', $stateParams.unitId, true);
        }]
      }
    });
  }]);
})();
