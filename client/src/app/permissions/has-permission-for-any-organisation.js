(function() {
  'use strict';

  var app = angular.module('radar.permissions');

  app.factory('hasPermissionForAnyOrganisation', ['_', function(_) {
    return function hasPermissionForAnyOrganisation(user, permission) {
      return (
        user !== null && (
          user.isAdmin ||
          _.any(user.organisations, function(x) {
            return x.hasPermission(permission);
          })
        )
      );
    };
  }]);
})();
