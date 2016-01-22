(function() {
  'use strict';

  var app = angular.module('radar.patients.genetics');

  app.config(['$stateProvider', function($stateProvider) {
    $stateProvider.state('patient.genetics', {
      url: '/genetics/:cohortId',
      templateUrl: 'app/patients/genetics/genetics.html',
      controller: ['$scope', 'cohort', function($scope, cohort) {
        $scope.cohort = cohort;
      }],
      resolve: {
        cohort: ['$stateParams', 'cohortStore', function($stateParams, cohortStore) {
          return cohortStore.findOne($stateParams.cohortId);
        }]
      }
    });
  }]);
})();
