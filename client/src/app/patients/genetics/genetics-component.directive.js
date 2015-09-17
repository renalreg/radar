(function() {
  'use strict';

  var app = angular.module('radar.patients.genetics');

  app.factory('GeneticsPermission', function(PatientObjectPermission) {
    return PatientObjectPermission;
  });

  app.factory('GeneticsController', function(DetailController, GeneticsPermission) {
    function GeneticsController($scope, $injector, store) {
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

    GeneticsController.prototype = Object.create(DetailController.prototype);

    return GeneticsController;
  });

  app.directive('geneticsComponent', function(GeneticsController) {
    return {
      scope: {
        patient: '=',
        cohort: '='
      },
      controller: GeneticsController,
      templateUrl: 'app/patients/genetics/genetics-component.html'
    };
  });
})();

