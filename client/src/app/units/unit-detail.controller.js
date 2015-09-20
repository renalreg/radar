(function() {
  'use strict';

  var app = angular.module('radar.units');

  app.controller('UnitDetailController', ['$scope', 'unit', function($scope, unit) {
    $scope.unit = unit;
  }]);
})();
