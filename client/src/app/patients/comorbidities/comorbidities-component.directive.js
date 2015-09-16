(function() {
  'use strict';

  var app = angular.module('radar.patients.medications');

  app.factory('ComorbidityPermission', function(PatientDataSourceObjectPermission) {
    return PatientDataSourceObjectPermission;
  });

  app.factory('ComorbiditiesController', function(ListDetailController, ComorbidityPermission, firstPromise) {
    function ComorbiditiesController($scope, $injector, $q, store) {
      var self = this;

      $injector.invoke(ListDetailController, self, {
        $scope: $scope,
        params: {
          permission: new ComorbidityPermission($scope.patient)
        }
      });

      self.load(firstPromise([
        store.findMany('comorbidities', {patient: $scope.patient.id}),
        store.findMany('comorbidity-disorders').then(function(disorders) {
          $scope.disorders = disorders;
        })
      ]));

      $scope.create = function() {
        var item = store.create('comorbidities', {patient: $scope.patient.id});
        self.edit(item);
      };
    }

    ComorbiditiesController.prototype = Object.create(ListDetailController.prototype);

    return ComorbiditiesController;
  });

  app.directive('comorbiditiesComponent', function(ComorbiditiesController) {
    return {
      scope: {
        patient: '='
      },
      controller: ComorbiditiesController,
      templateUrl: 'app/patients/comorbidities/comorbidities-component.html'
    };
  });
})();
