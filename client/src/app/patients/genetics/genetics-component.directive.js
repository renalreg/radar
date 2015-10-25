(function() {
  'use strict';

  var app = angular.module('radar.patients.genetics');

  app.factory('GeneticsPermission', ['PatientObjectPermission', function(PatientObjectPermission) {
    return PatientObjectPermission;
  }]);

  function controllerFactory(
    DetailController,
    GeneticsPermission,
    $injector,
    store
  ) {
    function GeneticsController($scope) {
      var self = this;

      $injector.invoke(DetailController, self, {
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
    GeneticsController.prototype = Object.create(DetailController.prototype);

    return GeneticsController;
  }

  controllerFactory.$inject = [
    'DetailController',
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
