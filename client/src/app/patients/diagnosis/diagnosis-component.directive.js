(function() {
  'use strict';

  var app = angular.module('radar.patients.diagnosis');

  app.factory('DiagnosisPermission', ['PatientObjectPermission', function(PatientObjectPermission) {
    return PatientObjectPermission;
  }]);

  function controllerFactory(
    ModelDetailController,
    DiagnosisPermission,
    firstPromise,
    $injector,
    store
  ) {
    function DiagnosisController($scope) {
      var self = this;

      $injector.invoke(ModelDetailController, self, {
        $scope: $scope,
        params: {
          permission: new DiagnosisPermission($scope.patient)
        }
      });

      self.load(firstPromise([
        store.findFirst('diagnoses', {patient: $scope.patient.id, cohort: $scope.cohort.id}),
        store.findMany('diagnosis-cohort-diagnoses', {cohort: $scope.cohort.id}).then(function(cohortDiagnoses) {
          $scope.cohortDiagnoses = cohortDiagnoses;
        }),
        store.findMany('diagnosis-biopsy-diagnoses').then(function(biopsyDiagnoses) {
          $scope.biopsyDiagnoses = biopsyDiagnoses;
        })
      ])).then(function() {
        self.view();
      });

      $scope.create = function() {
        var item = store.create('diagnoses', {patient: $scope.patient.id, cohort: $scope.cohort});
        self.edit(item);
      };
    }

    DiagnosisController.$inject = ['$scope'];
    DiagnosisController.prototype = Object.create(ModelDetailController.prototype);

    return DiagnosisController;
  }

  controllerFactory.$inject = [
    'ModelDetailController',
    'DiagnosisPermission',
    'firstPromise',
    '$injector',
    'store'
  ];

  app.factory('DiagnosisController', controllerFactory);

  app.directive('diagnosisComponent', ['DiagnosisController', function(DiagnosisController) {
    return {
      scope: {
        patient: '=',
        cohort: '='
      },
      controller: DiagnosisController,
      templateUrl: 'app/patients/diagnosis/diagnosis-component.html'
    };
  }]);
})();
