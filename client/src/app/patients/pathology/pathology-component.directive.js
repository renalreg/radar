(function() {
  'use strict';

  var app = angular.module('radar.patients.pathology');

  app.factory('PathologyPermission', ['PatientDataSourceObjectPermission', function(PatientDataSourceObjectPermission) {
    return PatientDataSourceObjectPermission;
  }]);

  function controllerFactory(
    ListDetailController,
    PathologyPermission,
    firstPromise,
    $injector,
    store
  ) {
    function PathologyController($scope) {
      var self = this;

      $injector.invoke(ListDetailController, self, {
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
    PathologyController.prototype = Object.create(ListDetailController.prototype);

    return PathologyController;
  }

  controllerFactory.$inject = [
    'ListDetailController',
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
