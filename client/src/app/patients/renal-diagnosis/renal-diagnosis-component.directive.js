(function() {
  'use strict';

  var app = angular.module('radar.patients.renalDiagnosis');

  app.factory('RenalDiagnosisPermission', ['PatientObjectPermission', function(PatientObjectPermission) {
    return PatientObjectPermission;
  }]);

  function controllerFactory(
    ModelDetailController,
    RenalDiagnosisPermission,
    $injector,
    store
  ) {
    function RenalDiagnosisController($scope) {
      var self = this;

      $injector.invoke(ModelDetailController, self, {
        $scope: $scope,
        params: {
          permission: new RenalDiagnosisPermission($scope.patient)
        }
      });

      self.load(store.findFirst('renal-diagnoses', {patient: $scope.patient.id})).then(function() {
        self.view();
      });

      $scope.create = function() {
        var item = store.create('renal-diagnoses', {patient: $scope.patient.id});
        self.edit(item);
      };
    }

    RenalDiagnosisController.$inject = ['$scope'];
    RenalDiagnosisController.prototype = Object.create(ModelDetailController.prototype);

    return RenalDiagnosisController;
  }

  controllerFactory.$inject = [
    'ModelDetailController',
    'RenalDiagnosisPermission',
    '$injector',
    'store'
  ];

  app.factory('RenalDiagnosisController', controllerFactory);

  app.directive('renalDiagnosisComponent', ['RenalDiagnosisController', function(RenalDiagnosisController) {
    return {
      scope: {
        patient: '='
      },
      controller: RenalDiagnosisController,
      templateUrl: 'app/patients/renal-diagnosis/renal-diagnosis-component.html'
    };
  }]);
})();
