(function() {
  'use strict';

  var app = angular.module('radar.patients.genetics');

  app.factory('GeneticsPermission', function(PatientDataPermission) {
    return PatientDataPermission;
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

      self.load(store.findMany('genetics', {patient: $scope.patient.id, cohort: $scope.cohort.id}).then(function(geneticsList) {
        if (geneticsList.length) {
          return geneticsList[0];
        } else {
          return null;
        }
      })).then(function() {
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

