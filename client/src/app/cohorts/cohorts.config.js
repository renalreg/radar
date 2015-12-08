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
        cohort: ['$stateParams', 'store', function($stateParams, store) {
          return store.findOne('cohorts', $stateParams.cohortId, true);
        }]
      }
    });
  }]);
})();
