(function() {
  'use strict';

  var app = angular.module('radar.patients.cohorts');

  app.factory('PatientUnitPermission', ['PatientObjectPermission', function(PatientObjectPermission) {
    return PatientObjectPermission;
  }]);

  function controllerFactory(
    ModelListDetailController,
    PatientUnitPermission,
    $injector,
    store
  ) {
    function PatientUnitsController($scope) {
      var self = this;

      $injector.invoke(ModelListDetailController, self, {
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

    PatientUnitsController.$inject = ['$scope'];
    PatientUnitsController.prototype = Object.create(ModelListDetailController.prototype);

    return PatientUnitsController;
  }

  controllerFactory.$inject = [
    'ModelListDetailController',
    'PatientUnitPermission',
    '$injector',
    'store'
  ];

  app.factory('PatientUnitsController', controllerFactory);

  app.directive('patientUnitsComponent', ['PatientUnitsController', function(PatientUnitsController) {
    return {
      scope: {
        patient: '='
      },
      controller: PatientUnitsController,
      templateUrl: 'app/patients/units/units-component.html'
    };
  }]);
})();
