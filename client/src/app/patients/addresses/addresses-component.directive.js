(function() {
  'use strict';

  var app = angular.module('radar.patients.addresses');

  app.factory('PatientAddressPermission', ['PatientRadarObjectPermission', function(PatientRadarObjectPermission) {
    return PatientRadarObjectPermission;
  }]);

  function controllerFactory(
    ModelListDetailController,
    PatientAddressPermission,
    firstPromise,
    getRadarDataSource,
    $injector,
    store
  ) {
    function PatientAddressesController($scope) {
      var self = this;

      $injector.invoke(ModelListDetailController, self, {
        $scope: $scope,
        params: {
          permission: new PatientAddressPermission($scope.patient)
        }
      });

      $scope.dataSource = null;

      self.load(firstPromise([
        store.findMany('patient-addresses', {patient: $scope.patient.id}),
        getRadarDataSource().then(function(dataSource) {
          $scope.dataSource = dataSource;
        })
      ]));

      $scope.create = function() {
        var item = store.create('patient-addresses', {
          patient: $scope.patient.id,
          dataSource: $scope.dataSource
        });
        self.edit(item);
      };
    }

    PatientAddressesController.$inject = ['$scope'];
    PatientAddressesController.prototype = Object.create(ModelListDetailController.prototype);

    return PatientAddressesController;
  }

  controllerFactory.$inject = [
    'ModelListDetailController',
    'PatientAddressPermission',
    'firstPromise',
    'getRadarDataSource',
    '$injector',
    'store'
  ];

  app.factory('PatientAddressesController', controllerFactory);

  app.directive('patientAddressesComponent', ['PatientAddressesController', function(PatientAddressesController) {
    return {
      scope: {
        patient: '='
      },
      controller: PatientAddressesController,
      templateUrl: 'app/patients/addresses/addresses-component.html'
    };
  }]);
})();
