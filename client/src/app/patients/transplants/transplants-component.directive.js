(function() {
  'use strict';

  var app = angular.module('radar.patients.transplants');

  app.factory('TransplantPermission', function(PatientDataSourceObjectPermission) {
    return PatientDataSourceObjectPermission;
  });

  app.factory('TransplantsController', function(ListDetailController, TransplantPermission) {
    function TransplantsController($scope, $injector, store) {
      var self = this;

      $injector.invoke(ListDetailController, self, {
        $scope: $scope,
        params: {
          permission: new TransplantPermission($scope.patient)
        }
      });

      self.load(store.findMany('transplants', {patient: $scope.patient.id}));

      $scope.create = function() {
        var item = store.create('transplants', {patient: $scope.patient.id});
        self.edit(item);
      };
    }

    TransplantsController.prototype = Object.create(ListDetailController.prototype);

    return TransplantsController;
  });

  app.directive('transplantsComponent', function(TransplantsController) {
    return {
      scope: {
        patient: '='
      },
      controller: TransplantsController,
      templateUrl: 'app/patients/transplants/transplants-component.html'
    };
  });
})();
