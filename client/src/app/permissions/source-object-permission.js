(function() {
  'use strict';

  var app = angular.module('radar.permissions');

  app.factory('SourceObjectPermission', ['session', 'hasPermissionForGroup', function(session, hasPermissionForGroup) {
    function SourceObjectPermission() {
    }

    SourceObjectPermission.prototype.hasPermission = function() {
      return true;
    };

    SourceObjectPermission.prototype.hasObjectPermission = function(obj) {
      if (!session.isAuthenticated) {
        return false;
      }

      var sourceType = obj.sourceType;

      if (sourceType !== 'RADAR') {
        return false;
      }

      var user = session.user;

      if (user.isAdmin) {
        return true;
      }

      var sourceGroup = obj.sourceGroup;

      return hasPermissionForGroup(user, sourceGroup, 'EDIT_PATIENT');
    };

    return SourceObjectPermission;
  }]);
})();
