(function() {
  'use strict';

  var app = angular.module('radar.permissions');

  app.factory('hasPermissionForOrganisation', ['_', function(_) {
    return function hasPermissionForOrganisation(user, organisation, permission) {
      return (
        user !== null && (
          user.isAdmin ||
          _.any(user.organisations, function(x) {
            return x.organisation.id === organisation.id && x.hasPermission(permission);
          })
        )
      );
    };
  }]);
})();
