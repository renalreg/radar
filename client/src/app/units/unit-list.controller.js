(function() {
  'use strict';

  var app = angular.module('radar.units');

  app.controller('UnitListController', ['$scope', 'session', 'store', '_', function($scope, session, store, _) {
    $scope.loading = true;

    var user = session.user;

    if (user.isAdmin) {
      store.findMany('organisations', {type: 'UNIT'}).then(function(units) {
        setUnits(units);
      });
    } else {
      setUnits(_.map(user.organisations, function(x) {
        return x.organisation;
      }));
    }

    function setUnits(units) {
      $scope.units = _.sortBy(units, 'name');
      $scope.loading = false;
    }
  }]);
})();
