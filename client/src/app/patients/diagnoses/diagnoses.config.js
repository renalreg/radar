(function() {
  'use strict';

  var app = angular.module('radar.patients.diagnoses');

  app.config(function($stateProvider) {
    $stateProvider.state('patient.diagnoses', {
      url: '/diagnoses/:cohortId',
      templateUrl: 'app/patients/diagnoses/diagnoses.html',
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
