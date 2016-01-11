(function() {
  'use strict';

  var app = angular.module('radar.cohorts');

  app.controller('CohortListController', ['$scope', 'session', 'store', '_', 'sortCohorts', function($scope, session, store, _, sortCohorts) {
    $scope.loading = true;

    init();

    function setCohorts(cohorts) {
      $scope.cohorts = sortCohorts(cohorts);
      $scope.loading = false;
    }

    function init() {
      var user = session.user;

      if (user.isAdmin) {
        // Admins can see all cohorts
        store.findMany('groups', {type: 'COHORT'}).then(function(cohorts) {
          setCohorts(cohorts);
        });
      } else {
        var cohorts = _.map(user.getCohorts(), function(x) {
          return x.cohort;
        });

        setCohorts(cohorts);
      }
    }
  }]);
})();
