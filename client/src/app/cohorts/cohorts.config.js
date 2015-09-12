(function() {
  'use strict';

  var app = angular.module('radar.cohorts');

  app.config(function($stateProvider) {
    $stateProvider.state('cohorts', {
      url: '/cohorts',
      templateUrl: 'app/cohorts/cohort-list.html'
    });

    $stateProvider.state('cohort', {
      url: '/cohorts/:cohortId',
      templateUrl: 'app/cohorts/cohort-detail.html'
    });
  });
})();
