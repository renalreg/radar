(function() {
  'use strict';

  var app = angular.module('radar.permissions');

  app.factory('SourceGroupObjectPermission', ['session', 'hasPermissionForGroup', function(session, hasPermissionForGroup) {
    function SourceGroupObjectPermission() {
    }

    SourceGroupObjectPermission.prototype.hasPermission = function() {
      return true;
    };

    SourceGroupObjectPermission.prototype.hasObjectPermission = function(obj) {
      if (!session.isAuthenticated) {
        return false;
      }

      var sourceType = obj.sourceType;

      if (sourceType.id !== 'RADAR') {
        return false;
      }

      var user = session.user;

      if (user.isAdmin) {
        return true;
      }

      var sourceGroup = obj.sourceGroup;

      return hasPermissionForGroup(user, sourceGroup, 'EDIT_PATIENT');
    };

    return SourceGroupObjectPermission;
  }]);
})();
