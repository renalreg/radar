(function() {
  'use strict';

  var app = angular.module('radar.patients.hospitals');

  app.factory('PatientHospitalPermission', ['hasPermission', 'hasPermissionForGroup', 'session', function(hasPermission, hasPermissionForGroup, session) {
    function PatientHospitalPermission() {
    }

    PatientHospitalPermission.prototype.hasPermission = function() {
      return hasPermission(session.user, 'EDIT_PATIENT_MEMBERSHIP');
    };

    PatientHospitalPermission.prototype.hasObjectPermission = function(obj) {
      return (
          hasPermissionForGroup(session.user, obj.group, 'EDIT_PATIENT_MEMBERSHIP') &&
          hasPermissionForGroup(session.user, obj.createdGroup, 'EDIT_PATIENT_MEMBERSHIP')
      );
    };

    return PatientHospitalPermission;
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
          permission: new PatientHospitalPermission()
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
        if (!_.includes(self.scope.patient.groups, groupPatient)) {
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
