(function() {
  'use strict';

  var app = angular.module('radar.patients.numbers');

  app.factory('PatientNumberPermission', ['PatientRadarObjectPermission', function(PatientRadarObjectPermission) {
    return PatientRadarObjectPermission;
  }]);

  app.factory('PatientNumbersController', ['ListDetailController', 'PatientNumberPermission', 'firstPromise', 'getRadarDataSource', '$injector', 'store', function(ListDetailController, PatientNumberPermission, firstPromise, getRadarDataSource, $injector, store) {
    function PatientNumbersController($scope) {
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

    PatientNumbersController.$inject = ['$scope'];
    PatientNumbersController.prototype = Object.create(ListDetailController.prototype);

    return PatientNumbersController;
  }]);

  app.directive('patientNumbersComponent', ['PatientNumbersController', function(PatientNumbersController) {
    return {
      scope: {
        patient: '='
      },
      controller: PatientNumbersController,
      templateUrl: 'app/patients/numbers/numbers-component.html'
    };
  }]);
})();
