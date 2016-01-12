(function() {
  'use strict';

  var app = angular.module('radar.patients.cohorts');

  app.factory('PatientCohortPermission', ['PatientObjectPermission', function(PatientObjectPermission) {
    return PatientObjectPermission;
  }]);

  function controllerFactory(
    ModelListDetailController,
    PatientCohortPermission,
    $injector,
    store,
    _
  ) {
    function PatientCohortsController($scope) {
      var self = this;

      $injector.invoke(ModelListDetailController, self, {
        $scope: $scope,
        params: {
          permission: new PatientCohortPermission($scope.patient)
        }
      });

      self.load($scope.patient.getCohorts());

      $scope.create = function() {
        self.edit(store.create('group-patients', {patient: $scope.patient.id}));
      };
    }

    PatientCohortsController.$inject = ['$scope'];
    PatientCohortsController.prototype = Object.create(ModelListDetailController.prototype);

    PatientCohortsController.prototype.save = function() {
      var self = this;

      return ModelListDetailController.prototype.save.call(self).then(function(groupPatient) {
        // Add the group to the patient's groups
        if (!_.contains(self.scope.patient.groups, groupPatient)) {
          self.scope.patient.groups.push(groupPatient);
        }

        return groupPatient;
      });
    };

    PatientCohortsController.prototype.remove = function(groupPatient) {
      var self = this;

      return ModelListDetailController.prototype.remove.call(self, groupPatient).then(function() {
        // Remove the group from the patient's groups
        _.pull(self.scope.patient.groups, groupPatient);
      });
    };

    return PatientCohortsController;
  }

  controllerFactory.$inject = [
    'ModelListDetailController',
    'PatientCohortPermission',
    '$injector',
    'store',
    '_'
  ];

  app.factory('PatientCohortsController', controllerFactory);

  app.directive('patientCohortsComponent', ['PatientCohortsController', function(PatientCohortsController) {
    return {
      scope: {
        patient: '='
      },
      controller: PatientCohortsController,
      templateUrl: 'app/patients/cohorts/cohorts-component.html'
    };
  }]);
})();
