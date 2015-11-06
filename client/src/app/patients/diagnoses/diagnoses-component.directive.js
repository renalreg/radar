(function() {
  'use strict';

  var app = angular.module('radar.patients.diagnoses');

  app.factory('DiagnosisPermission', ['PatientObjectPermission', function(PatientObjectPermission) {
    return PatientObjectPermission;
  }]);

  function controllerFactory(
    ModelListDetailController,
    DiagnosisPermission,
    firstPromise,
    $injector,
    store
  ) {
    function DiagnosesController($scope) {
      var self = this;

      $injector.invoke(ModelListDetailController, self, {
        $scope: $scope,
        params: {
          permission: new DiagnosisPermission($scope.patient)
        }
      });

      self.load(firstPromise([
        store.findMany('diagnoses', {patient: $scope.patient.id, cohort: $scope.cohort.id}),
        store.findMany('medication-dose-units').then(function(doseUnits) {
          $scope.doseUnits = doseUnits;
        }),
        store.findMany('diagnosis-cohort-diagnoses', {cohort: $scope.cohort.id}).then(function(cohortDiagnoses) {
          $scope.cohortDiagnoses = cohortDiagnoses;
        }),
        store.findMany('diagnosis-biopsy-diagnoses').then(function(biopsyDiagnoses) {
          $scope.biopsyDiagnoses = biopsyDiagnoses;
        })
      ]));

      $scope.create = function() {
        var item = store.create('diagnoses', {patient: $scope.patient.id, cohort: $scope.cohort});
        self.edit(item);
      };
    }

    DiagnosesController.$inject = ['$scope'];
    DiagnosesController.prototype = Object.create(ModelListDetailController.prototype);

    return DiagnosesController;
  }

  controllerFactory.$inject = [
    'ModelListDetailController',
    'DiagnosisPermission',
    'firstPromise',
    '$injector',
    'store'
  ];

  app.factory('DiagnosesController', controllerFactory);

  app.directive('diagnosesComponent', ['DiagnosesController', function(DiagnosesController) {
    return {
      scope: {
        patient: '=',
        cohort: '='
      },
      controller: DiagnosesController,
      templateUrl: 'app/patients/diagnoses/diagnoses-component.html'
    };
  }]);
})();
