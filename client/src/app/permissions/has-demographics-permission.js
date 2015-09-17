(function() {
  'use strict';

  var app = angular.module('radar.permissions');

  app.factory('hasDemographicsPermission', function(_) {
    return function hasDemographicsPermission(patient, user) {
      var i;

      if (user.isAdmin) {
        return true;
      }

      var patientOrganisationIds = _.map(patient.organisations, function(organisation) {
        return organisation.organisation.id;
      });

      var userOrganisations = user.organisations;

      for (i = 0; i < userOrganisations.length; i++) {
        var userOrganisation = userOrganisations[i];

        if (_.indexOf(patientOrganisationIds, userOrganisation.organisation.id) >= 0 && userOrganisation.hasViewDemographicsPermission) {
          return true;
        }
      }

      var patientCohortIds = _.map(patient.cohorts, function(cohort) {
        return cohort.cohort.id;
      });

      var userCohorts = user.cohorts;

      for (i = 0; i < userCohorts.length; i++) {
        var userCohort = userCohorts[i];

        if (_.indexOf(patientCohortIds, userCohort.cohort.id) >= 0 && userCohort.hasViewDemographicsPermission) {
          return true;
        }
      }

      return false;
    };
  });
})();

