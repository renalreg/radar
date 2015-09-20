(function() {
  'use strict';

  var app = angular.module('radar.patients.cohorts');

  app.factory('PatientCohortPermission', ['PatientObjectPermission', function(PatientObjectPermission) {
    return PatientObjectPermission;
  }]);

  app.factory('PatientCohortsController', ['ListDetailController', 'PatientCohortPermission', '$injector', 'store', function(ListDetailController, PatientCohortPermission, $injector, store) {
    function PatientCohortsController($scope) {
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

    PatientCohortsController.$inject = ['$scope'];
    PatientCohortsController.prototype = Object.create(ListDetailController.prototype);

    return PatientCohortsController;
  }]);

  app.directive('patientCohortsComponent', ['PatientCohortsController', function(PatientCohortsController) {
    return {
      scope: {
        patient: '='
      },
      controller: PatientCohortsController,
      templateUrl: 'app/patients/cohorts/cohorts-component.html'
    };
  }]);
})();

