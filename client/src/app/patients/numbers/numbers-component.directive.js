(function() {
  'use strict';

  var app = angular.module('radar.patients.demographics');

  app.factory('PatientNumberPermission', function(PatientRadarObjectPermission) {
    return PatientRadarObjectPermission;
  });

  app.factory('PatientNumbersController', function(ListDetailController, PatientNumberPermission, firstPromise, getRadarDataSource) {
    function PatientNumbersController($scope, $injector, store) {
      var self = this;

      $injector.invoke(ListDetailController, self, {
        $scope: $scope,
        params: {
          permission: new PatientNumberPermission($scope.patient)
        }
      });

      $scope.dataSource = null;

      self.load(firstPromise([
        store.findMany('patient-numbers', {patient: $scope.patient.id}),
        getRadarDataSource().then(function(dataSource) {
          $scope.dataSource = dataSource;
        })
      ]));

      $scope.create = function() {
        var item = store.create('patient-numbers', {
          patient: $scope.patient.id,
          dataSource: $scope.dataSource
        });
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
      templateUrl: 'app/patients/numbers/numbers-component.html'
    };
  });
})();
