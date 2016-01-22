(function() {
  'use strict';

  var app = angular.module('radar.permissions');

  app.factory('PatientObjectPermission', ['session', 'hasPermissionForPatient', function(session, hasPermissionForPatient) {
    function PatientObjectPermission(patient) {
      this.patient = patient;
    }

    PatientObjectPermission.prototype.hasPermission = function() {
      if (!session.isAuthenticated) {
        return false;
      }

      var user = session.user;

      return hasPermissionForPatient(user, this.patient, 'EDIT_PATIENT');
    };

    PatientObjectPermission.prototype.hasObjectPermission = function() {
      return this.hasPermission();
    };

    return PatientObjectPermission;
  }]);
})();
