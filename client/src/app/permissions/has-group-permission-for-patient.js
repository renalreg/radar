(function() {
  'use strict';

  var app = angular.module('radar.permissions');

  function factory(
    hasCohortPermissionForPatient,
    hasOrganisationPermissionForPatient
  ) {
    return function hasGroupPermissionForPatient(user, patient, permission) {
      return (
        user !== null && (
          user.isAdmin ||
          hasCohortPermissionForPatient(user, patient, permission) ||
          hasOrganisationPermissionForPatient(user, patient, permission)
        )
      );
    };
  }

  factory.$inject = [
    'hasCohortPermissionForPatient',
    'hasOrganisationPermissionForPatient'
  ];

  app.factory('hasGroupPermissionForPatient', factory);
})();
