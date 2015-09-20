(function() {
  'use strict';

  var app = angular.module('radar.cohorts');

  app.controller('CohortDetailController', ['$scope', 'cohort', function($scope, cohort) {
    $scope.cohort = cohort;
  }]);
})();
