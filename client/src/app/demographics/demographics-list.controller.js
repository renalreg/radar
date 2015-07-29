(function() {
  'use strict';

  var app = angular.module('radar.demographics');

  app.controller('DemographicsListController', function($scope, items) {
    $scope.items = items;
  });
})();
