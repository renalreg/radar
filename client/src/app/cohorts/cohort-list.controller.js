(function() {
  'use strict';

  var app = angular.module('radar.cohorts');

  app.controller('CohortListController', function($scope, cohorts, _) {
    $scope.cohorts = _.sortBy(cohorts, 'name');
  });
})();
