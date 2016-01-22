(function() {
  'use strict';

  var app = angular.module('radar.patients.diagnoses');

  app.config(['$stateProvider', function($stateProvider) {
    $stateProvider.state('patient.diagnoses', {
      url: '/diagnoses',
      templateUrl: 'app/patients/diagnoses/diagnoses.html'
    });

    $stateProvider.state('patient.primaryDiagnosis', {
      url: '/primary-diagnosis/:cohortId',
      templateUrl: 'app/patients/diagnoses/primary-diagnosis.html',
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
