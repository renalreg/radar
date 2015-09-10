(function() {
  'use strict';

  var app = angular.module('radar.patients.genetics');

  app.config(function($stateProvider) {
    $stateProvider.state('patient.genetics', {
      url: '/genetics/:diseaseGroupId',
      templateUrl: 'app/patients/genetics/genetics.html',
      controller: function($scope, diseaseGroup) {
        $scope.diseaseGroup = diseaseGroup;
      },
      resolve: {
        diseaseGroup: function($stateParams, store) {
          return store.findOne('disease-groups', $stateParams.diseaseGroupId, true);
        }
      }
    });
  });
})();
