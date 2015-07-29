(function() {
  'use strict';

  var app = angular.module('radar');

  app.controller('DialysisListController', function($scope, model) {
    $scope.model = model;
  });
})();
