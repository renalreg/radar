(function() {
  'use strict';

  var app = angular.module('radar.patients.diagnoses');

  function controllerFactory(
    ModelListDetailController,
    PatientDiagnosisPermission,
    firstPromise,
    $injector,
    store,
    _,
    getRadarGroup
  ) {
    function PrimaryPatientDiagnosisController($scope) {
      var self = this;

      $injector.invoke(ModelListDetailController, self, {
        $scope: $scope,
        params: {
          permission: new PatientDiagnosisPermission($scope.patient)
        }
      });

      self.load(firstPromise([
        store.findMany('patient-diagnoses', {patient: $scope.patient.id}),
        store.findMany('diagnoses').then(function(diagnoses) {
          $scope.diagnoses = diagnoses;
        }),
        store.findMany('biopsy-diagnoses').then(function(biopsyDiagnoses) {
          $scope.biopsyDiagnoses = biopsyDiagnoses;
        }),
        getRadarGroup().then(function(group) {
          $scope.sourceGroup = group;
        })
      ]));

      $scope.create = function() {
        var item = store.create('patient-diagnoses', {
          patient: $scope.patient.id,
          sourceGroup: $scope.sourceGroup,
        });
        self.edit(item);
      };
    }

    PrimaryPatientDiagnosisController.$inject = ['$scope'];
    PrimaryPatientDiagnosisController.prototype = Object.create(ModelListDetailController.prototype);

    return PrimaryPatientDiagnosisController;
  }

  controllerFactory.$inject = [
    'ModelListDetailController',
    'PatientDiagnosisPermission',
    'firstPromise',
    '$injector',
    'store',
    '_',
    'getRadarGroup'
  ];

  app.factory('PrimaryPatientDiagnosisController', controllerFactory);

  app.directive('primaryPatientDiagnosisComponent', ['PrimaryPatientDiagnosisController', function(PrimaryPatientDiagnosisController) {
    return {
      scope: {
        patient: '=',
        cohort: '='
      },
      controller: PrimaryPatientDiagnosisController,
      templateUrl: 'app/patients/diagnoses/primary-diagnosis-component.html'
    };
  }]);
})();
