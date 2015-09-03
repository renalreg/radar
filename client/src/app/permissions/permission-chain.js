(function() {
  'use strict';

  var app = angular.module('radar.permissions');

  app.factory('PermissionChain', function() {
    function PermissionChain(permissions) {
      this.permissions = permissions;
    }

    PermissionChain.prototype.hasPermission = function() {
      return this.run(function(permission) {
        return permission.hasPermission();
      });
    };

    PermissionChain.prototype.hasObjectPermission = function(obj) {
      return this.run(function(permission) {
        return permission.hasObjectPermission(obj);
      });
    };

    PermissionChain.prototype.run = function(callback) {
      for (var i = 0; i < this.permissions.length; i++) {
        var permission = this.permissions[i];

        if (!callback(permission)) {
          return false;
        }
      }

      return true;
    };

    return PermissionChain;
  });
})();
