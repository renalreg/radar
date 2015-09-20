(function() {
  'use strict';

  var app = angular.module('radar.cohorts');

  app.config(['$stateProvider', function($stateProvider) {
    $stateProvider.state('cohorts', {
      url: '/cohorts',
      templateUrl: 'app/cohorts/cohort-list.html',
      controller: 'CohortListController',
      resolve: {
        cohorts: ['store', 'session', '_', function(store, session, _) {
          var user = session.user;

          if (user.isAdmin) {
            return store.findMany('cohorts');
          } else {
            return _.map(user.cohorts, function(x) {
              return x.cohort;
            });
          }
        }]
      }
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
