(function() {
  'use strict';

  var app = angular.module('radar.patients.ins');

  app.factory('InsRelapsePermission', ['PatientObjectPermission', function(PatientObjectPermission) {
    return PatientObjectPermission;
  }]);

  function controllerFactory(
    ModelListDetailController,
    InsRelapsePermission,
    firstPromise,
    $injector,
    store
  ) {
    function InsRelapsesController($scope) {
      var self = this;

      $injector.invoke(ModelListDetailController, self, {
        $scope: $scope,
        params: {
          permission: new InsRelapsePermission($scope.patient)
        }
      });

      self.load(firstPromise([
        store.findMany('ins-relapses', {patient: $scope.patient.id}),
        store.findMany('ins-kidney-types').then(function(kidneyTypes) {
          $scope.kidneyTypes = kidneyTypes;
        }),
        store.findMany('ins-remission-types').then(function(remissionTypes) {
          $scope.remissionTypes = remissionTypes;
        })
      ]));

      $scope.create = function() {
        var item = store.create('ins-relapses', {patient: $scope.patient.id});
        self.edit(item);
      };
    }

    InsRelapsesController.$inject = ['$scope'];
    InsRelapsesController.prototype = Object.create(ModelListDetailController.prototype);

    return InsRelapsesController;
  }

  controllerFactory.$inject = [
    'ModelListDetailController',
    'InsRelapsePermission',
    'firstPromise',
    '$injector',
    'store'
  ];

  app.factory('InsRelapsesController', controllerFactory);

  app.directive('insRelapsesComponent', ['InsRelapsesController', function(InsRelapsesController) {
    return {
      scope: {
        patient: '='
      },
      controller: InsRelapsesController,
      templateUrl: 'app/patients/ins/relapses-component.html'
    };
  }]);
})();
