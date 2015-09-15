(function() {
  'use strict';

  var app = angular.module('radar.patients.aliases');

  app.factory('PatientAliasPermission', function(PatientDataSourceObjectPermission) {
    return PatientDataSourceObjectPermission;
  });

  app.factory('PatientAliasesController', function(ListDetailController, PatientAliasPermission) {
    function PatientAliasesController($scope, $injector, store) {
      var self = this;

      $injector.invoke(ListDetailController, self, {
        $scope: $scope,
        params: {
          permission: new PatientAliasPermission($scope.patient)
        }
      });

      self.load(store.findMany('patient-aliases', {patient: $scope.patient.id}));

      $scope.create = function() {
        var item = store.create('patient-aliases', {patient: $scope.patient.id});
        self.edit(item);
      };
    }

    PatientAliasesController.prototype = Object.create(ListDetailController.prototype);

    return PatientAliasesController;
  });

  app.directive('patientAliasesComponent', function(PatientAliasesController) {
    return {
      scope: {
        patient: '='
      },
      controller: PatientAliasesController,
      templateUrl: 'app/patients/aliases/aliases-component.html'
    };
  });
})();
