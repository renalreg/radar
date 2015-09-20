(function() {
  'use strict';

  var app = angular.module('radar.patients.plasmapheresis');

  app.factory('PlasmapheresisPermission', ['PatientDataSourceObjectPermission', function(PatientDataSourceObjectPermission) {
    return PatientDataSourceObjectPermission;
  }]);

  app.factory('PlasmapheresisController', ['ListDetailController', 'PlasmapheresisPermission', 'firstPromise', '$injector', 'store', function(ListDetailController, PlasmapheresisPermission, firstPromise, $injector, store) {
    function PlasmapheresisController($scope) {
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
        }),
        store.findMany('plasmapheresis-no-of-exchanges').then(function(noOfExchanges) {
          $scope.noOfExchanges = noOfExchanges;
        })
      ]));

      $scope.create = function() {
        var item = store.create('plasmapheresis', {patient: $scope.patient.id});
        self.edit(item);
      };
    }

    PlasmapheresisController.$inject = ['$scope'];
    PlasmapheresisController.prototype = Object.create(ListDetailController.prototype);

    return PlasmapheresisController;
  }]);

  app.directive('plasmapheresisComponent', ['PlasmapheresisController', function(PlasmapheresisController) {
    return {
      scope: {
        patient: '='
      },
      controller: PlasmapheresisController,
      templateUrl: 'app/patients/plasmapheresis/plasmapheresis-component.html'
    };
  }]);
})();
