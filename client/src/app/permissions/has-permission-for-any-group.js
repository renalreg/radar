(function() {
  'use strict';

  var app = angular.module('radar.permissions');

  app.factory('hasPermissionForAnyGroup', ['_', function(_) {
    return function hasPermissionForAnyGroup(user, permission) {
      return (
        user !== null && (
          user.isAdmin ||
          _.any(user.groups, function(x) {
            return x.hasPermission(permission);
          })
        )
      );
    };
  }]);
})();
