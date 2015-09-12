(function() {
  'use strict';

  var app = angular.module('radar.patients.genetics');

  app.config(function($stateProvider) {
    $stateProvider.state('patient.genetics', {
      url: '/genetics/:cohortId',
      templateUrl: 'app/patients/genetics/genetics.html',
      controller: function($scope, cohort) {
        $scope.cohort = cohort;
      },
      resolve: {
        cohort: function($stateParams, store) {
          return store.findOne('cohorts', $stateParams.cohortId, true);
        }
      }
    });
  });
})();
