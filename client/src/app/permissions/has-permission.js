(function() {
  'use strict';

  var app = angular.module('radar.permissions');

  app.factory('hasPermission', ['_', function(_) {
    return function hasPermission(user, permission) {
      return (
        user !== null && (
          user.isAdmin ||
          _.some(user.groups, function(x) {
            return x.hasPermission(permission);
          })
        )
      );
    };
  }]);
})();
