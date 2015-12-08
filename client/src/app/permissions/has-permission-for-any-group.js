(function() {
  'use strict';

  var app = angular.module('radar.permissions');

  function factory(
    hasPermissionForAnyCohort,
    hasPermissionForAnyOrganisation
  ) {
    return function hasPermissionForAnyGroup(user, permission) {
      return (
        user !== null &&
        (
          user.isAdmin ||
          hasPermissionForAnyCohort(user, permission) ||
          hasPermissionForAnyOrganisation(user, permission)
        )
      );
    };
  }

  factory.$inject = [
    'hasPermissionForAnyCohort',
    'hasPermissionForAnyOrganisation'
  ];

  app.factory('hasPermissionForAnyGroup', factory);
})();
