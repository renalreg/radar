(function() {
  'use strict';

  var app = angular.module('radar.patients.demographics');

  app.factory('PatientDemographicsPermission', ['PatientRadarObjectPermission', function(PatientRadarObjectPermission) {
    return PatientRadarObjectPermission;
  }]);

  function controllerFactory(
    ListDetailController,
    PatientDemographicsPermission,
    firstPromise,
    DenyPermission,
    $injector,
    store
  ) {
    function PatientDemographicsController($scope) {
      var self = this;

      $injector.invoke(ListDetailController, self, {
        $scope: $scope,
        params: {
          createPermission: new DenyPermission(),
          editPermission: new PatientDemographicsPermission($scope.patient),
          removePermission: new DenyPermission()
        }
      });

      self.load(firstPromise([
        store.findMany('patient-demographics', {patient: $scope.patient.id}),
        store.findMany('genders').then(function(genders) {
          $scope.genders = genders;
        }),
        store.findMany('ethnicity-codes').then(function(ethnicityCodes) {
          $scope.ethnicityCodes = ethnicityCodes;
        })
      ]));
    }

    PatientDemographicsController.$inject = ['$scope'];
    PatientDemographicsController.prototype = Object.create(ListDetailController.prototype);

    PatientDemographicsController.prototype.save = function() {
      var self = this;

      return ListDetailController.prototype.save.call(self).then(function() {
        // Reload the patient with the latest demographics
        self.scope.patient.reload();
      });
    };

    return PatientDemographicsController;
  }

  controllerFactory.$inject = [
    'ListDetailController',
    'PatientDemographicsPermission',
    'firstPromise',
    'DenyPermission',
    '$injector',
    'store'
  ];

  app.factory('PatientDemographicsController', controllerFactory);

  app.directive('patientDemographicsComponent', ['PatientDemographicsController', function(PatientDemographicsController) {
    return {
      scope: {
        patient: '='
      },
      controller: PatientDemographicsController,
      templateUrl: 'app/patients/demographics/demographics-component.html'
    };
  }]);
})();
