(function() {
  'use strict';

  var app = angular.module('radar.patients.cohorts');

  app.config(['$stateProvider', function($stateProvider) {
    $stateProvider.state('patient.cohorts', {
      url: '/cohorts',
      templateUrl: 'app/patients/cohorts/cohorts.html'
    });

    $stateProvider.state('patient.cohort', {
      url: '/cohorts/:cohortId',
      templateUrl: 'app/patients/cohorts/cohort.html',
      controller: ['$scope', 'cohort', function($scope, cohort) {
        $scope.cohort = cohort;
      }],
      resolve: {
        cohort: ['$stateParams', 'store', function($stateParams, store) {
          return store.findOne('cohorts', $stateParams.cohortId, true);
        }]
      }
    });
  }]);
})();
