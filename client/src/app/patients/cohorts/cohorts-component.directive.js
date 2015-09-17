(function() {
  'use strict';

  var app = angular.module('radar.patients.cohorts');

  app.factory('PatientCohortPermission', function(PatientObjectPermission) {
    return PatientObjectPermission;
  });

  app.factory('PatientCohortsController', function(ListDetailController, PatientCohortPermission) {
    function PatientCohortsController($scope, $injector, store) {
      var self = this;

      $injector.invoke(ListDetailController, self, {
        $scope: $scope,
        params: {
          permission: new PatientCohortPermission($scope.patient)
        }
      });

      self.load($scope.patient.cohorts);

      $scope.create = function() {
        self.edit(store.create('cohort-patients', {patient: $scope.patient.id, isActive: true}));
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
