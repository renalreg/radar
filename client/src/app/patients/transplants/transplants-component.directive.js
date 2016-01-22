(function() {
  'use strict';

  var app = angular.module('radar.patients.transplants');

  app.factory('TransplantPermission', ['PatientSourceObjectPermission', function(PatientSourceObjectPermission) {
    return PatientSourceObjectPermission;
  }]);

  function controllerFactory(
    ModelListDetailController,
    TransplantPermission,
    firstPromise,
    $injector,
    store
  ) {
    function TransplantsController($scope) {
      var self = this;

      $injector.invoke(ModelListDetailController, self, {
        $scope: $scope,
        params: {
          permission: new TransplantPermission($scope.patient)
        }
      });

      self.load(firstPromise([
        store.findMany('transplants', {patient: $scope.patient.id}),
        store.findMany('transplant-modalities').then(function(modalities) {
          $scope.modalities = modalities;
        })
      ]));

      $scope.create = function() {
        var item = store.create('transplants', {patient: $scope.patient.id});
        self.edit(item);
      };
    }

    TransplantsController.$inject = ['$scope'];
    TransplantsController.prototype = Object.create(ModelListDetailController.prototype);

    return TransplantsController;
  }

  controllerFactory.$inject = [
    'ModelListDetailController',
    'TransplantPermission',
    'firstPromise',
    '$injector',
    'store',
  ];

  app.factory('TransplantsController', controllerFactory);

  app.directive('transplantsComponent', ['TransplantsController', function(TransplantsController) {
    return {
      scope: {
        patient: '='
      },
      controller: TransplantsController,
      templateUrl: 'app/patients/transplants/transplants-component.html'
    };
  }]);
})();
