(function() {
  'use strict';

  var app = angular.module('radar.patients.demographics');

  app.factory('PatientAliasPermission', function(PatientFacilityDataPermission) {
    return PatientFacilityDataPermission;
  });

  app.factory('PatientAliasesController', function(ListDetailController, PatientAliasPermission) {
    function PatientAliasesController($scope, $injector, store) {
      var self = this;

      $injector.invoke(ListDetailController, self, {
        $scope: $scope,
        params: {
          permission: new PatientAliasPermission($scope.patient)
        }
      });

      self.load(store.findMany('patient-aliases', {patientId: $scope.patient.id}));

      $scope.create = function() {
        var item = store.create('patient-aliases', {patientId: $scope.patient.id});
        self.edit(item);
      };
    }

    PatientAliasesController.prototype = Object.create(ListDetailController.prototype);

    return PatientAliasesController;
  });

  app.directive('patientAliasesComponent', function(PatientAliasesController) {
    return {
      scope: {
        patient: '='
      },
      controller: PatientAliasesController,
      templateUrl: 'app/patients/demographics/aliases-component.html'
    };
  });
})();
