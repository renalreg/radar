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

      if (user.isAdmin) {
        return true;
      }

      var patient = this.patient;
      var patientUnitIds = _.map(patient.units, function(unit) {
        return unit.unit.id;
      });

      var userUnits = user.units;

      for (var i = 0; i < user.units; i++) {
        var userUnit = userUnits[i];

        if (_.indexOf(patientUnitIds, userUnit.unit.id) >= 0) {
          return userUnit.hasEditPatientPermission;
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
