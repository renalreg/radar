(function() {
  'use strict';

  var app = angular.module('radar.patients.plasmapheresis');

  app.factory('PlasmapheresisPermission', function(PatientFacilityDataPermission) {
    return PatientFacilityDataPermission;
  });

  app.factory('PlasmapheresisController', function(ListDetailController, PlasmapheresisPermission) {
    function PlasmapheresisController($scope, $injector, $q, store) {
      var self = this;

      $injector.invoke(ListDetailController, self, {
        $scope: $scope,
        params: {
          permission: $injector.instantiate(PlasmapheresisPermission, {patient: $scope.patient})
        }
      });

      var items = [];

      $q.all([
        store.findMany('plasmapheresis', {patientId: $scope.patient.id}).then(function(plasmapheresisList) {
          items = plasmapheresisList;
        }),
        store.findMany('plasmapheresis-responses').then(function(responses) {
          $scope.responses = responses;
        })
      ]).then(function() {
        self.load(items);
      });

      $scope.create = function() {
        var item = store.create('plasmapheresis', {patientId: $scope.patient.id});
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

