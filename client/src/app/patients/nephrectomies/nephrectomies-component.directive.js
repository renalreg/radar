(function() {
  'use strict';

  var app = angular.module('radar.patients.nephrectomies');

  app.factory('NephrectomyPermission', ['PatientDataSourceObjectPermission', function(PatientDataSourceObjectPermission) {
    return PatientDataSourceObjectPermission;
  }]);

  function controllerFactory(
    ListDetailController,
    NephrectomyPermission,
    firstPromise,
    $injector,
    store
  ) {
    function NephrectomiesController($scope) {
      var self = this;

      $injector.invoke(ListDetailController, self, {
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
    NephrectomiesController.prototype = Object.create(ListDetailController.prototype);

    return NephrectomiesController;
  }

  controllerFactory.$inject = [
    'ListDetailController',
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
