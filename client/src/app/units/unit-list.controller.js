(function() {
  'use strict';

  var app = angular.module('radar.units');

  app.controller('UnitListController', ['$scope', 'units', '_', function($scope, units, _) {
    $scope.units = _.sortBy(units, 'name');
  }]);
})();
