(function() {
  'use strict';

  var app = angular.module('radar.patients.genetics');

  app.factory('GeneticsPermission', ['PatientObjectPermission', function(PatientObjectPermission) {
    return PatientObjectPermission;
  }]);

  function controllerFactory(
    ModelDetailController,
    GeneticsPermission,
    $injector,
    store
  ) {
    function GeneticsController($scope) {
      var self = this;

      $injector.invoke(ModelDetailController, self, {
        $scope: $scope,
        params: {
          permission: new GeneticsPermission($scope.patient)
        }
      });

      self.load(store.findFirst('genetics', {patient: $scope.patient.id, cohort: $scope.cohort.id})).then(function() {
        self.view();
      });

      $scope.create = function() {
        var item = store.create('genetics', {patient: $scope.patient.id, cohort: $scope.cohort});
        self.edit(item);
      };
    }

    GeneticsController.$inject = ['$scope'];
    GeneticsController.prototype = Object.create(ModelDetailController.prototype);

    return GeneticsController;
  }

  controllerFactory.$inject = [
    'ModelDetailController',
    'GeneticsPermission',
    '$injector',
    'store'
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
