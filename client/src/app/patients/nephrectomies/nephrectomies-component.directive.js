(function() {
  'use strict';

  var app = angular.module('radar.patients.nephrectomies');

  app.factory('NephrectomyPermission', ['PatientSourceObjectPermission', function(PatientSourceObjectPermission) {
    return PatientSourceObjectPermission;
  }]);

  function controllerFactory(
    ModelListDetailController,
    NephrectomyPermission,
    firstPromise,
    $injector,
    store
  ) {
    function NephrectomiesController($scope) {
      var self = this;

      $injector.invoke(ModelListDetailController, self, {
        $scope: $scope,
        params: {
          permission: new NephrectomyPermission($scope.patient)
        }
      });

      self.load(firstPromise([
        store.findMany('nephrectomies', {patient: $scope.patient.id}),
        store.findMany('nephrectomy-kidney-sides').then(function(kidneySides) {
          $scope.kidneySides = kidneySides;
        }),
        store.findMany('nephrectomy-kidney-types').then(function(kidneyTypes) {
          $scope.kidneyTypes = kidneyTypes;
        }),
        store.findMany('nephrectomy-entry-types').then(function(entryTypes) {
          $scope.entryTypes = entryTypes;
        })
      ]));

      $scope.create = function() {
        var item = store.create('nephrectomies', {patient: $scope.patient.id});
        self.edit(item);
      };
    }

    NephrectomiesController.$inject = ['$scope'];
    NephrectomiesController.prototype = Object.create(ModelListDetailController.prototype);

    return NephrectomiesController;
  }

  controllerFactory.$inject = [
    'ModelListDetailController',
    'NephrectomyPermission',
    'firstPromise',
    '$injector',
    'store'
  ];

  app.factory('NephrectomiesController', controllerFactory);

  app.directive('nephrectomiesComponent', ['NephrectomiesController', function(NephrectomiesController) {
    return {
      scope: {
        patient: '='
      },
      controller: NephrectomiesController,
      templateUrl: 'app/patients/nephrectomies/nephrectomies-component.html'
    };
  }]);
})();
