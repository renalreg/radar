(function() {
  'use strict';

  var app = angular.module('radar.patients.dialysis');

  app.factory('DialysisPermission', ['PatientDataSourceObjectPermission', function(PatientDataSourceObjectPermission) {
    return PatientDataSourceObjectPermission;
  }]);

  function controllerFactory(
    ModelListDetailController,
    DialysisPermission,
    firstPromise,
    $injector,
    store
  ) {
    function DialysisController($scope) {
      var self = this;

      $injector.invoke(ModelListDetailController, self, {
        $scope: $scope,
        params: {
          permission: new DialysisPermission($scope.patient)
        }
      });

      self.load(firstPromise([
        store.findMany('dialysis', {patient: $scope.patient.id}),
        store.findMany('dialysis-modalities').then(function(modalities) {
          $scope.modalities = modalities;
        })
      ]));

      $scope.create = function() {
        var item = store.create('dialysis', {patient: $scope.patient.id});
        self.edit(item);
      };
    }

    DialysisController.$inject = ['$scope'];
    DialysisController.prototype = Object.create(ModelListDetailController.prototype);

    return DialysisController;
  }

  controllerFactory.$inject = [
    'ModelListDetailController',
    'DialysisPermission',
    'firstPromise',
    '$injector',
    'store'
  ];

  app.factory('DialysisController', controllerFactory);

  app.directive('dialysisComponent', ['DialysisController', function(DialysisController) {
    return {
      scope: {
        patient: '='
      },
      controller: DialysisController,
      templateUrl: 'app/patients/dialysis/dialysis-component.html'
    };
  }]);
})();
