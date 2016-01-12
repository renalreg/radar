(function() {
  'use strict';

  var app = angular.module('radar.patients.numbers');

  app.factory('PatientNumberPermission', ['PatientRadarObjectPermission', function(PatientRadarObjectPermission) {
    return PatientRadarObjectPermission;
  }]);

  function controllerFactory(
    ModelListDetailController,
    PatientNumberPermission,
    firstPromise,
    getRadarGroup,
    $injector,
    store
  ) {
    function PatientNumbersController($scope) {
      var self = this;

      $injector.invoke(ModelListDetailController, self, {
        $scope: $scope,
        params: {
          permission: new PatientNumberPermission($scope.patient)
        }
      });

      $scope.sourceGroup = null;

      self.load(firstPromise([
        store.findMany('patient-numbers', {patient: $scope.patient.id}),
        getRadarGroup().then(function(group) {
          $scope.sourceGroup = group;
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
    PatientNumbersController.prototype = Object.create(ModelListDetailController.prototype);

    return PatientNumbersController;
  }

  controllerFactory.$inject = [
    'ModelListDetailController',
    'PatientNumberPermission',
    'firstPromise',
    'getRadarGroup',
    '$injector',
    'store'
  ];

  app.factory('PatientNumbersController', controllerFactory);

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
