(function() {
  'use strict';

  var app = angular.module('radar.patients.demographics');

  app.factory('PatientNumberPermission', function(PatientFacilityDataPermission) {
    return PatientFacilityDataPermission;
  });

  app.factory('PatientNumbersController', function(ListDetailController, PatientNumberPermission) {
    function PatientNumbersController($scope, $injector, store) {
      var self = this;

      $injector.invoke(ListDetailController, self, {
        $scope: $scope,
        params: {
          permission: new PatientNumberPermission($scope.patient)
        }
      });

      self.load(store.findMany('patient-numbers', {patientId: $scope.patient.id}));

      $scope.create = function() {
        var item = store.create('patient-numbers', {patientId: $scope.patient.id});
        self.edit(item);
      };
    }

    PatientNumbersController.prototype = Object.create(ListDetailController.prototype);

    return PatientNumbersController;
  });

  app.directive('patientNumbersComponent', function(PatientNumbersController) {
    return {
      scope: {
        patient: '='
      },
      controller: PatientNumbersController,
      templateUrl: 'app/patients/demographics/numbers-component.html'
    };
  });
})();

