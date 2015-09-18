(function() {
  'use strict';

  var app = angular.module('radar.patients.cohorts');

  app.factory('PatientUnitPermission', function(PatientObjectPermission) {
    return PatientObjectPermission;
  });

  app.factory('PatientUnitsController', function(ListDetailController, PatientUnitPermission) {
    function PatientUnitsController($scope, $injector, store) {
      var self = this;

      $injector.invoke(ListDetailController, self, {
        $scope: $scope,
        params: {
          permission: new PatientUnitPermission($scope.patient)
        }
      });

      self.load($scope.patient.organisations);

      $scope.create = function() {
        self.edit(store.create('organisation-patients', {patient: $scope.patient.id, isActive: true}));
      };
    }

    PatientUnitsController.prototype = Object.create(ListDetailController.prototype);

    return PatientUnitsController;
  });

  app.directive('patientUnitsComponent', function(PatientUnitsController) {
    return {
      scope: {
        patient: '='
      },
      controller: PatientUnitsController,
      templateUrl: 'app/patients/units/units-component.html'
    };
  });
})();
