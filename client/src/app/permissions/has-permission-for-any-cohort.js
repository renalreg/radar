(function() {
  'use strict';

  var app = angular.module('radar.permissions');

  app.factory('hasPermissionForAnyCohort', ['_', function(_) {
    return function hasPermissionForAnyCohort(user, permission) {
      return (
        user !== null && (
          user.isAdmin ||
          _.any(user.cohorts, function(x) {
            return x.hasPermission(permission);
          })
        )
      );
    };
  }]);
})();
