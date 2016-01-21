(function() {
  'use strict';

  var app = angular.module('radar.patients.diagnoses');

  function controllerFactory(
    ModelListDetailController,
    PatientDiagnosisPermission,
    $injector,
    store
  ) {
    function PatientDiagnosesController($scope) {
      var self = this;

      $injector.invoke(ModelListDetailController, self, {
        $scope: $scope,
        params: {
          permission: new PatientDiagnosisPermission($scope.patient)
        }
      });

      self.load(store.findMany('patient-diagnoses', {patient: $scope.patient.id}));

      $scope.create = function() {
        var item = store.create('patient-diagnoses', {patient: $scope.patient.id});
        self.edit(item);
      };
    }

    PatientDiagnosesController.$inject = ['$scope'];
    PatientDiagnosesController.prototype = Object.create(ModelListDetailController.prototype);

    return PatientDiagnosesController;
  }

  controllerFactory.$inject = [
    'ModelListDetailController',
    'PatientDiagnosisPermission',
    '$injector',
    'store'
  ];

  app.factory('PatientDiagnosesController', controllerFactory);

  app.directive('patientDiagnosesComponent', ['PatientDiagnosesController', function(PatientDiagnosesController) {
    return {
      scope: {
        patient: '='
      },
      controller: PatientDiagnosesController,
      templateUrl: 'app/patients/diagnoses/diagnoses-component.html'
    };
  }]);
})();
