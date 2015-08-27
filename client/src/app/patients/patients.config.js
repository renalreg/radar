(function() {
  'use strict';

  var app = angular.module('radar.patients');

  app.config(function($stateProvider) {
    $stateProvider.state('patients', {
      url: '/patients',
      templateUrl: 'app/patients/patient-list.html',
      controller: function($scope, $controller, PatientListController) {
        $controller(PatientListController, {$scope: $scope});
      }
    });

    $stateProvider.state('patient', {
      url: '/patients/:patientId',
      abstract: true,
      templateUrl: 'app/patients/patient-detail.html',
      controller: 'PatientDetailController',
      resolve: {
        patient: function($stateParams, store) {
          return store.findOne('patients', $stateParams.patientId);
        }
      }
    });
  });
})();
