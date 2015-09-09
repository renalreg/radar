(function() {
  'use strict';

  var app = angular.module('radar.permissions');

  app.factory('PatientDataPermission', function(session, _) {
    function PatientDataPermission(patient) {
      this.patient = patient;
    }

    PatientDataPermission.prototype.hasPermission = function() {
      if (!session.isAuthenticated) {
        return false;
      }

      var user = session.user;

      var patient = this.patient;
      var patientUnitIds = _.map(patient.units, function(unit) {
        return unit.unit.id;
      });

      if (user.isAdmin && patientUnitIds.length > 0) {
        return true;
      }

      var userUnits = user.units;

      for (var i = 0; i < userUnits.length; i++) {
        var userUnit = userUnits[i];

        if (_.indexOf(patientUnitIds, userUnit.unit.id) >= 0 && userUnit.hasEditPatientPermission) {
          return true;
        }
      }

      return false;
    };

    PatientDataPermission.prototype.hasObjectPermission = function() {
      return this.hasPermission();
    };

    return PatientDataPermission;
  });
})();
