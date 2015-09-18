(function() {
  'use strict';

  var app = angular.module('radar.cohorts');

  app.controller('CohortDetailController', function($scope, cohort) {
    $scope.cohort = cohort;
  });
})();
