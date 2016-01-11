(function() {
  'use strict';

  var app = angular.module('radar.patients.demographics');

  app.factory('PatientDemographicsPermission', ['PatientRadarSourceGroupObjectPermission', function(PatientRadarSourceGroupObjectPermission) {
    return PatientRadarSourceGroupObjectPermission;
  }]);

  function controllerFactory(
    ModelListDetailController,
    PatientDemographicsPermission,
    firstPromise,
    DenyPermission,
    $injector,
    store
  ) {
    function PatientDemographicsController($scope) {
      var self = this;

      $injector.invoke(ModelListDetailController, self, {
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
        store.findMany('ethnicities').then(function(ethnicities) {
          $scope.ethnicities = ethnicities;
        })
      ]));
    }

    PatientDemographicsController.$inject = ['$scope'];
    PatientDemographicsController.prototype = Object.create(ModelListDetailController.prototype);

    PatientDemographicsController.prototype.save = function() {
      var self = this;

      return ModelListDetailController.prototype.save.call(self).then(function() {
        // Reload the patient with the latest demographics
        self.scope.patient.reload();
      });
    };

    return PatientDemographicsController;
  }

  controllerFactory.$inject = [
    'ModelListDetailController',
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
