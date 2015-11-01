(function() {
  'use strict';

  var app = angular.module('radar.patients.medications');

  app.factory('MedicationPermission', ['PatientDataSourceObjectPermission', function(PatientDataSourceObjectPermission) {
    return PatientDataSourceObjectPermission;
  }]);

  function controllerFactory(
    ModelListDetailController,
    MedicationPermission,
    firstPromise,
    $injector,
    store
  ) {
    function MedicationsController($scope) {
      var self = this;

      $injector.invoke(ModelListDetailController, self, {
        $scope: $scope,
        params: {
          permission: new MedicationPermission($scope.patient)
        }
      });

      self.load(firstPromise([
        store.findMany('medications', {patient: $scope.patient.id}),
        store.findMany('medication-dose-units').then(function(doseUnits) {
          $scope.doseUnits = doseUnits;
        }),
        store.findMany('medication-frequencies').then(function(frequencies) {
          $scope.frequencies = frequencies;
        }),
        store.findMany('medication-routes').then(function(routes) {
          $scope.routes = routes;
        })
      ]));

      $scope.create = function() {
        var item = store.create('medications', {patient: $scope.patient.id});
        self.edit(item);
      };
    }

    MedicationsController.$inject = ['$scope'];
    MedicationsController.prototype = Object.create(ModelListDetailController.prototype);

    return MedicationsController;
  }

  controllerFactory.$inject = [
    'ModelListDetailController',
    'MedicationPermission',
    'firstPromise',
    '$injector',
    'store'
  ];

  app.factory('MedicationsController', controllerFactory);

  app.directive('medicationsComponent', ['MedicationsController', function(MedicationsController) {
    return {
      scope: {
        patient: '='
      },
      controller: MedicationsController,
      templateUrl: 'app/patients/medications/medications-component.html'
    };
  }]);
})();