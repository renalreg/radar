(function() {
  'use strict';

  var app = angular.module('radar.units');

  app.controller('UnitListController', function($scope, units, _) {
    $scope.units = _.sortBy(units, 'name');
  });
})();
