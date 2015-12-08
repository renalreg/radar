(function() {
  'use strict';

  var app = angular.module('radar.permissions');

  app.factory('hasOrganisationPermissionForPatient', ['_', function(_) {
    return function hasOrganisationPermissionForPatient(user, patient, permission) {
      if (user === null) {
        return false;
      }

      if (user.isAdmin) {
        return true;
      }

      var patientOrganisationIds = _.map(patient.organisations, function(organisation) {
        return organisation.organisation.id;
      });

      var userOrganisations = user.organisations;

      for (var i = 0; i < userOrganisations.length; i++) {
        var userOrganisation = userOrganisations[i];

        if (_.indexOf(patientOrganisationIds, userOrganisation.organisation.id) >= 0 && userOrganisation.hasPermission(permission)) {
          return true;
        }
      }

      return false;
    };
  }]);
})();
