(function() {
  'use strict';

  var app = angular.module('radar.patients.hospitals');

  app.factory('PatientHospitalPermission', ['PatientObjectPermission', function(PatientObjectPermission) {
    return PatientObjectPermission;
  }]);

  function controllerFactory(
    ModelListDetailController,
    PatientHospitalPermission,
    $injector,
    store,
    _
  ) {
    function PatientHospitalsController($scope) {
      var self = this;

      $injector.invoke(ModelListDetailController, self, {
        $scope: $scope,
        params: {
          permission: new PatientHospitalPermission($scope.patient)
        }
      });

      self.load($scope.patient.getHospitals());

      $scope.create = function() {
        self.edit(store.create('group-patients', {patient: $scope.patient.id}));
      };
    }

    PatientHospitalsController.$inject = ['$scope'];
    PatientHospitalsController.prototype = Object.create(ModelListDetailController.prototype);

    PatientHospitalsController.prototype.save = function() {
      var self = this;

      return ModelListDetailController.prototype.save.call(self).then(function(groupPatient) {
        // Add the group to the patient's groups
        if (!_.contains(self.scope.patient.groups, groupPatient)) {
          self.scope.patient.groups.push(groupPatient);
        }

        return groupPatient;
      });
    };

    PatientHospitalsController.prototype.remove = function(groupPatient) {
      var self = this;

      return ModelListDetailController.prototype.remove.call(self, groupPatient).then(function() {
        // Remove the group from the patient's groups
        _.pull(self.scope.patient.groups, groupPatient);
      });
    };

    return PatientHospitalsController;
  }

  controllerFactory.$inject = [
    'ModelListDetailController',
    'PatientHospitalPermission',
    '$injector',
    'store',
    '_'
  ];

  app.factory('PatientHospitalsController', controllerFactory);

  app.directive('patientHospitalsComponent', ['PatientHospitalsController', function(PatientHospitalsController) {
    return {
      scope: {
        patient: '='
      },
      controller: PatientHospitalsController,
      templateUrl: 'app/patients/hospitals/hospitals-component.html'
    };
  }]);
})();
