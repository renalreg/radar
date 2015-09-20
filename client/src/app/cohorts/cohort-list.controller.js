(function() {
  'use strict';

  var app = angular.module('radar.cohorts');

  app.controller('CohortListController', ['$scope', 'cohorts', '_', function($scope, cohorts, _) {
    $scope.cohorts = _.sortBy(cohorts, 'name');
  }]);
})();
