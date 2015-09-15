(function() {
  'use strict';

  var app = angular.module('radar.patients.addresses');

  app.factory('PatientAddressPermission', function(PatientDataSourceObjectPermission) {
    return PatientDataSourceObjectPermission;
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

      self.load(store.findMany('patient-addresses', {patient: $scope.patient.id}));

      $scope.create = function() {
        var item = store.create('patient-addresses', {patient: $scope.patient.id});
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
      templateUrl: 'app/patients/addresses/addresses-component.html'
    };
  });
})();

