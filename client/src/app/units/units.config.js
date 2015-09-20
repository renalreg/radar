(function() {
  'use strict';

  var app = angular.module('radar.units');

  app.config(['$stateProvider', function($stateProvider) {
    $stateProvider.state('units', {
      url: '/units',
      templateUrl: 'app/units/unit-list.html',
      controller: 'UnitListController',
      resolve: {
        units: ['store', 'session', '_', function(store, session, _) {
          var user = session.user;

          if (user.isAdmin) {
            return store.findMany('organisations', {type: 'UNIT'});
          } else {
            return _.map(user.organisations, function(x) {
              return x.organisation;
            });
          }
        }]
      }
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
