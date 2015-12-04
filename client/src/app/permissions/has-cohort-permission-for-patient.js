(function() {
  'use strict';

  var app = angular.module('radar.permissions');

  app.factory('hasCohortPermissionForPatient', ['_', function(_) {
    return function hasCohortPermissionForPatient(user, patient, permission) {
      if (user === null) {
        return false;
      }

      if (user.isAdmin) {
        return true;
      }

      var patientCohortIds = _.map(patient.cohorts, function(cohort) {
        return cohort.cohort.id;
      });

      var userCohorts = user.cohorts;

      for (var i = 0; i < userCohorts.length; i++) {
        var userCohort = userCohorts[i];

        if (_.indexOf(patientCohortIds, userCohort.cohort.id) >= 0 && userCohort.hasPermission(permission)) {
          return true;
        }
      }

      return false;
    };
  }]);
})();
