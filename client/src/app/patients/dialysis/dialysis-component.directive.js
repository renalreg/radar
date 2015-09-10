(function() {
  'use strict';

  var app = angular.module('radar.patients.dialysis');

  app.factory('DialysisPermission', function(PatientFacilityDataPermission) {
    return PatientFacilityDataPermission;
  });

  app.factory('DialysisController', function(ListDetailController, DialysisPermission, firstPromise) {
    function DialysisController($scope, $injector, store) {
      var self = this;

      $injector.invoke(ListDetailController, self, {
        $scope: $scope,
        params: {
          permission: new DialysisPermission($scope.patient)
        }
      });

      self.load(firstPromise([
        store.findMany('dialysis', {patientId: $scope.patient.id}),
        store.findMany('dialysis-types').then(function(dialysisTypes) {
          $scope.dialysisTypes = dialysisTypes;
        })
      ]));

      $scope.create = function() {
        var item = store.create('dialysis', {patientId: $scope.patient.id});
        self.edit(item);
      };
    }

    DialysisController.prototype = Object.create(ListDetailController.prototype);

    return DialysisController;
  });

  app.directive('dialysisComponent', function(DialysisController) {
    return {
      scope: {
        patient: '='
      },
      controller: DialysisController,
      templateUrl: 'app/patients/dialysis/dialysis-component.html'
    };
  });
})();
