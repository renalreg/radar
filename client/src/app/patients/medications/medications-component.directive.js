(function() {
  'use strict';

  var app = angular.module('radar.patients.medications');

  app.factory('MedicationPermission', function(PatientFacilityDataPermission) {
    return PatientFacilityDataPermission;
  });

  app.factory('MedicationsController', function(ListDetailController, MedicationPermission) {
    function MedicationsController($scope, $injector, $q, store) {
      var self = this;

      $injector.invoke(ListDetailController, self, {
        $scope: $scope,
        params: {
          permission: $injector.instantiate(MedicationPermission, {patient: $scope.patient})
        }
      });

      var items = [];

      $q.all([
        store.findMany('medications', {patientId: $scope.patient.id}).then(function(medications) {
          items = medications;
        }),
        store.findMany('medication-dose-units').then(function(doseUnits) {
          $scope.doseUnits = doseUnits;
        }),
        store.findMany('medication-frequencies').then(function(frequencies) {
          $scope.frequencies = frequencies;
        }),
        store.findMany('medication-routes').then(function(routes) {
          $scope.routes = routes;
        })
      ]).then(function() {
        self.load(items);
      });

      $scope.create = function() {
        var item = store.create('medications', {patientId: $scope.patient.id});
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
