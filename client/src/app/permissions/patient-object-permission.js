(function() {
  'use strict';

  var app = angular.module('radar.permissions');

  app.factory('PatientObjectPermission', function(session, _) {
    function PatientObjectPermission(patient) {
      this.patient = patient;
    }

    PatientObjectPermission.prototype.hasPermission = function() {
      if (!session.isAuthenticated) {
        return false;
      }

      var user = session.user;

      var patient = this.patient;
      var patientOrganisationIds = _.map(patient.organisations, function(organisation) {
        return organisation.organisation.id;
      });

      if (user.isAdmin && patientOrganisationIds.length > 0) {
        return true;
      }

      var userOrganisations = user.organisations;

      for (var i = 0; i < userOrganisations.length; i++) {
        var userOrganisation = userOrganisations[i];

        if (_.indexOf(patientOrganisationIds, userOrganisation.organisation.id) >= 0 && userOrganisation.hasEditPatientPermission) {
          return true;
        }
      }

      return false;
    };

    PatientObjectPermission.prototype.hasObjectPermission = function() {
      return this.hasPermission();
    };

    return PatientObjectPermission;
  });
})();
