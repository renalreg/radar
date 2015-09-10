(function() {
  'use strict';

  var app = angular.module('radar.patients.demographics');

  app.factory('PatientAddressPermission', function(PatientFacilityDataPermission) {
    return PatientFacilityDataPermission;
  });

  app.factory('PatientAddressesController', function(ListDetailController, PatientAddressPermission) {
    function PatientAddressesController($scope, $injector, store) {
      var self = this;

      $injector.invoke(ListDetailController, self, {
        $scope: $scope,
        params: {
          permission: new PatientAddressPermission($scope.patient)
        }
      });

      self.load(store.findMany('patient-addresses', {patientId: $scope.patient.id}));

      $scope.create = function() {
        var item = store.create('patient-addresses', {patientId: $scope.patient.id});
        self.edit(item);
      };
    }

    PatientAddressesController.prototype = Object.create(ListDetailController.prototype);

    return PatientAddressesController;
  });

  app.directive('patientAddressesComponent', function(PatientAddressesController) {
    return {
      scope: {
        patient: '='
      },
      controller: PatientAddressesController,
      templateUrl: 'app/patients/demographics/addresses-component.html'
    };
  });
})();

