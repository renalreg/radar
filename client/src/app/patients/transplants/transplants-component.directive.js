(function() {
  'use strict';

  var app = angular.module('radar.patients.transplants');

  app.factory('TransplantPermission', ['PatientDataSourceObjectPermission', function(PatientDataSourceObjectPermission) {
    return PatientDataSourceObjectPermission;
  }]);

  app.factory('TransplantsController', ['ListDetailController', 'TransplantPermission', 'firstPromise', '$injector', 'store', function(ListDetailController, TransplantPermission, firstPromise, $injector, store) {
    function TransplantsController($scope) {
      var self = this;

      $injector.invoke(ListDetailController, self, {
        $scope: $scope,
        params: {
          permission: new TransplantPermission($scope.patient)
        }
      });

      self.load(firstPromise([
        store.findMany('transplants', {patient: $scope.patient.id}),
        store.findMany('transplant-types').then(function(transplantTypes) {
          $scope.transplantTypes = transplantTypes;
        })
      ]));

      $scope.create = function() {
        var item = store.create('transplants', {patient: $scope.patient.id});
        self.edit(item);
      };
    }

    TransplantsController.$inject = ['$scope'];
    TransplantsController.prototype = Object.create(ListDetailController.prototype);

    return TransplantsController;
  }]);

  app.directive('transplantsComponent', ['TransplantsController', function(TransplantsController) {
    return {
      scope: {
        patient: '='
      },
      controller: TransplantsController,
      templateUrl: 'app/patients/transplants/transplants-component.html'
    };
  }]);
})();
