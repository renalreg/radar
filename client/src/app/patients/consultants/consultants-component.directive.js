(function() {
  'use strict';

  var app = angular.module('radar.patients.consultants');

  app.factory('PatientConsultantPermission', ['PatientObjectPermission', function(PatientObjectPermission) {
    return PatientObjectPermission;
  }]);

  function controllerFactory(
    ModelListDetailController,
    PatientConsultantPermission,
    firstPromise,
    $injector,
    store
  ) {
    function PatientConsultantsController($scope) {
      var self = this;

      $injector.invoke(ModelListDetailController, self, {
        $scope: $scope,
        params: {
          permission: new PatientConsultantPermission($scope.patient)
        }
      });

      self.load(firstPromise([
        store.findMany('patient-consultants', {patient: $scope.patient.id}),
        store.findMany('consultants', {patient: $scope.patient.id}).then(function(consultants) {
          $scope.consultants = consultants;
        })
      ]));

      $scope.create = function() {
        var item = store.create('patient-consultants', {patient: $scope.patient.id});
        self.edit(item);
      };
    }

    PatientConsultantsController.$inject = ['$scope'];
    PatientConsultantsController.prototype = Object.create(ModelListDetailController.prototype);

    return PatientConsultantsController;
  }

  controllerFactory.$inject = [
    'ModelListDetailController',
    'PatientConsultantPermission',
    'firstPromise',
    '$injector',
    'store'
  ];

  app.factory('PatientConsultantsController', controllerFactory);

  app.directive('patientConsultantsComponent', ['PatientConsultantsController', function(PatientConsultantsController) {
    return {
      scope: {
        patient: '='
      },
      controller: PatientConsultantsController,
      templateUrl: 'app/patients/consultants/consultants-component.html'
    };
  }]);
})();
