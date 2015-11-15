(function() {
  'use strict';

  var app = angular.module('radar.permissions');

  app.factory('AdminPermission', ['session', function(session) {
    function AdminPermission() {
    }

    AdminPermission.prototype.hasPermission = function() {
      return session.isAuthenticated && session.user.isAdmin;
    };

    AdminPermission.prototype.hasObjectPermission = function(obj) {
      return session.isAuthenticated && session.user.isAdmin;
    };

    return AdminPermission;
  }]);
})();
