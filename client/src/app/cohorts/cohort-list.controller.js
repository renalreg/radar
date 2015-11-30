(function() {
  'use strict';

  var app = angular.module('radar.cohorts');

  app.controller('CohortListController', ['$scope', 'session', 'store', '_', function($scope, session, store, _) {
    $scope.loading = true;

    var user = session.user;

    if (user.isAdmin) {
      store.findMany('cohorts').then(function(cohorts) {
        setCohorts(cohorts);
      });
    } else {
      setCohorts(_.map(user.cohorts, function(x) {
        return x.cohort;
      }));
    }

    function setCohorts(cohorts) {
      $scope.cohorts = _.sortBy(cohorts, 'name');
      $scope.loading = false;
    }
  }]);
})();
