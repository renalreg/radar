(function() {
  'use strict';

  var app = angular.module('radar.patients.genetics');

  app.factory('GeneticsPermission', ['PatientObjectPermission', function(PatientObjectPermission) {
    return PatientObjectPermission;
  }]);

  function controllerFactory(
    ModelListDetailController,
    GeneticsPermission,
    $injector,
    store,
    firstPromise
  ) {
    function GeneticsController($scope) {
      var self = this;

      $injector.invoke(ModelListDetailController, self, {
        $scope: $scope,
        params: {
          permission: new GeneticsPermission($scope.patient)
        }
      });

      self.load(firstPromise([
        store.findMany('genetics', {patient: $scope.patient.id, cohort: $scope.cohort.id}),
        store.findMany('genetics-karyotypes').then(function(karyotypes) {
          $scope.karyotypes = karyotypes;
        })
      ]));

      $scope.create = function() {
        var item = store.create('genetics', {patient: $scope.patient.id, cohort: $scope.cohort});
        self.edit(item);
      };
    }

    GeneticsController.$inject = ['$scope'];
    GeneticsController.prototype = Object.create(ModelListDetailController.prototype);

    return GeneticsController;
  }

  controllerFactory.$inject = [
    'ModelListDetailController',
    'GeneticsPermission',
    '$injector',
    'store',
    'firstPromise'
  ];

  app.factory('GeneticsController', controllerFactory);

  app.directive('geneticsComponent', ['GeneticsController', function(GeneticsController) {
    return {
      scope: {
        patient: '=',
        cohort: '='
      },
      controller: GeneticsController,
      templateUrl: 'app/patients/genetics/genetics-component.html'
    };
  }]);
})();
