(function() {
  'use strict';

  var app = angular.module('radar.permissions');

  app.factory('hasPermissionForGroup', ['_', function(_) {
    return function hasPermissionForGroup(user, group, permission) {
      return (
        user !== null && (
          user.isAdmin ||
          _.some(user.groups, function(x) {
            return x.group.id === group.id && x.hasPermission(permission);
          })
        )
      );
    };
  }]);
})();
