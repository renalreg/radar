(function() {
  'use strict';

  var app = angular.module('radar.patients.pathology');

  app.factory('PathologyPermission', ['PatientSourceGroupObjectPermission', function(PatientSourceGroupObjectPermission) {
    return PatientSourceGroupObjectPermission;
  }]);

  function controllerFactory(
    ModelListDetailController,
    PathologyPermission,
    firstPromise,
    $injector,
    store
  ) {
    function PathologyController($scope) {
      var self = this;

      $injector.invoke(ModelListDetailController, self, {
        $scope: $scope,
        params: {
          permission: new PathologyPermission($scope.patient)
        }
      });

      self.load(firstPromise([
        store.findMany('pathology', {patient: $scope.patient.id}),
        store.findMany('pathology-kidney-types').then(function(kidneyTypes) {
          $scope.kidneyTypes = kidneyTypes;
        }),
        store.findMany('pathology-kidney-sides').then(function(kidneySides) {
          $scope.kidneySides = kidneySides;
        })
      ]));

      $scope.create = function() {
        var item = store.create('pathology', {patient: $scope.patient.id});
        self.edit(item);
      };
    }

    PathologyController.$inject = ['$scope'];
    PathologyController.prototype = Object.create(ModelListDetailController.prototype);

    return PathologyController;
  }

  controllerFactory.$inject = [
    'ModelListDetailController',
    'PathologyPermission',
    'firstPromise',
    '$injector',
    'store'
  ];

  app.factory('PathologyController', controllerFactory);

  app.directive('pathologyComponent', ['PathologyController', function(PathologyController) {
    return {
      scope: {
        patient: '='
      },
      controller: PathologyController,
      templateUrl: 'app/patients/pathology/pathology-component.html'
    };
  }]);
})();
