(function() {
  'use strict';

  var app = angular.module('radar.patients.cohorts');

  app.factory('PatientCohortsController', function(ListDetailController) {
    function PatientCohortsController($scope, $injector, store) {
      var self = this;

      $injector.invoke(ListDetailController, self, {$scope: $scope, params: {}});

      self.load($scope.patient.cohorts);

      $scope.create = function() {
        self.edit(store.create('patient-cohorts', {patient: $scope.patient.id}));
      };
    }

    PatientCohortsController.prototype = Object.create(ListDetailController.prototype);

    return PatientCohortsController;
  });

  app.directive('patientCohortsComponent', function(PatientCohortsController) {
    return {
      scope: {
        patient: '='
      },
      controller: PatientCohortsController,
      templateUrl: 'app/patients/cohorts/cohorts-component.html'
    };
  });
})();

