(function() {
  'use strict';

  var app = angular.module('radar.patients.plasmapheresis');

  app.factory('PlasmapheresisPermission', function(PatientDataSourceObjectPermission) {
    return PatientDataSourceObjectPermission;
  });

  app.factory('PlasmapheresisController', function(ListDetailController, PlasmapheresisPermission, firstPromise) {
    function PlasmapheresisController($scope, $injector, store) {
      var self = this;

      $injector.invoke(ListDetailController, self, {
        $scope: $scope,
        params: {
          permission: new PlasmapheresisPermission($scope.patient)
        }
      });

      self.load(firstPromise([
        store.findMany('plasmapheresis', {patient: $scope.patient.id}),
        store.findMany('plasmapheresis-responses').then(function(responses) {
          $scope.responses = responses;
        })
      ]));

      $scope.create = function() {
        var item = store.create('plasmapheresis', {patient: $scope.patient.id});
        self.edit(item);
      };
    }

    PlasmapheresisController.prototype = Object.create(ListDetailController.prototype);

    return PlasmapheresisController;
  });

  app.directive('plasmapheresisComponent', function(PlasmapheresisController) {
    return {
      scope: {
        patient: '='
      },
      controller: PlasmapheresisController,
      templateUrl: 'app/patients/plasmapheresis/plasmapheresis-component.html'
    };
  });
})();

