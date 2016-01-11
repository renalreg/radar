(function() {
  'use strict';

  var app = angular.module('radar.cohorts');

  app.config(['$stateProvider', function($stateProvider) {
    $stateProvider.state('cohorts', {
      url: '/cohorts',
      templateUrl: 'app/cohorts/cohort-list.html',
      controller: 'CohortListController'
    });

    $stateProvider.state('cohort', {
      url: '/cohorts/:cohortId',
      templateUrl: 'app/cohorts/cohort-detail.html',
      controller: 'CohortDetailController',
      resolve: {
        cohort: ['$stateParams', 'store', '$q', function($stateParams, store, $q) {
          return store.findOne('groups', $stateParams.cohortId, true).then(function(group) {
            if (group.type === 'COHORT') {
              return group;
            } else {
              return $q.reject();
            }
          });
        }]
      }
    });
  }]);
})();
