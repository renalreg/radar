(function() {
  'use strict';

  var app = angular.module('radar.patients.medications');

  app.factory('MedicationPermission', function(PatientDataSourceObjectPermission) {
    return PatientDataSourceObjectPermission;
  });

  app.factory('MedicationsController', function(ListDetailController, MedicationPermission, firstPromise) {
    function MedicationsController($scope, $injector, store) {
      var self = this;

      $injector.invoke(ListDetailController, self, {
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

    MedicationsController.prototype = Object.create(ListDetailController.prototype);

    return MedicationsController;
  });

  app.directive('medicationsComponent', function(MedicationsController) {
    return {
      scope: {
        patient: '='
      },
      controller: MedicationsController,
      templateUrl: 'app/patients/medications/medications-component.html'
    };
  });
})();
