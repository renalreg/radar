(function() {
  'use strict';

  var app = angular.module('radar.patients.aliases');

  app.factory('PatientAliasPermission', ['PatientRadarSourceGroupObjectPermission', function(PatientRadarSourceGroupObjectPermission) {
    return PatientRadarSourceGroupObjectPermission;
  }]);

  function controllerFactory(
    ModelListDetailController,
    PatientAliasPermission,
    firstPromise,
    getRadarDataSource,
    $injector,
    store
  ) {
    function PatientAliasesController($scope) {
      var self = this;

      $injector.invoke(ModelListDetailController, self, {
        $scope: $scope,
        params: {
          permission: new PatientAliasPermission($scope.patient)
        }
      });

      self.load(firstPromise([
        store.findMany('patient-aliases', {patient: $scope.patient.id}),
        getRadarDataSource().then(function(dataSource) {
          $scope.dataSource = dataSource;
        })
      ]));

      $scope.create = function() {
        var item = store.create('patient-aliases', {
          patient: $scope.patient.id,
          dataSource: $scope.dataSource
        });
        self.edit(item);
      };
    }

    PatientAliasesController.$inject = ['$scope'];
    PatientAliasesController.prototype = Object.create(ModelListDetailController.prototype);

    return PatientAliasesController;
  }

  controllerFactory.$inject = [
    'ModelListDetailController',
    'PatientAliasPermission',
    'firstPromise',
    'getRadarDataSource',
    '$injector',
    'store'
  ];

  app.factory('PatientAliasesController', controllerFactory);

  app.directive('patientAliasesComponent', ['PatientAliasesController', function(PatientAliasesController) {
    return {
      scope: {
        patient: '='
      },
      controller: PatientAliasesController,
      templateUrl: 'app/patients/aliases/aliases-component.html'
    };
  }]);
})();
