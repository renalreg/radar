(function() {
  'use strict';

  var app = angular.module('radar.patients.demographics');

  app.factory('PatientDemographicsPermission', function(PatientDataSourceObjectPermission) {
    return PatientDataSourceObjectPermission;
  });

  app.factory('PatientDemographicsController', function(ListDetailController, PatientDemographicsPermission, firstPromise) {
    function PatientDemographicsController($scope, $injector, store) {
      var self = this;

      $injector.invoke(ListDetailController, self, {
        $scope: $scope,
        params: {
          permission: new PatientDemographicsPermission($scope.patient)
        }
      });

      self.load(firstPromise([
        store.findMany('patient-demographics', {patient: $scope.patient.id}),
        store.findMany('ethnicity-codes').then(function(ethnicityCodes) {
          $scope.ethnicityCodes = ethnicityCodes;
        })
      ]));

      $scope.create = function() {
        var item = store.create('patient-demographics', {patient: $scope.patient.id});
        self.edit(item);
      };
    }

    PatientDemographicsController.prototype = Object.create(ListDetailController.prototype);

    return PatientDemographicsController;
  });

  app.directive('patientDemographicsComponent', function(PatientDemographicsController) {
    return {
      scope: {
        patient: '='
      },
      controller: PatientDemographicsController,
      templateUrl: 'app/patients/demographics/demographics-component.html'
    };
  });
})();
