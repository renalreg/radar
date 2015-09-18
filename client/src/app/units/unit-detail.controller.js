(function() {
  'use strict';

  var app = angular.module('radar.units');

  app.controller('UnitDetailController', function($scope, unit) {
    $scope.unit = unit;
  });
})();
