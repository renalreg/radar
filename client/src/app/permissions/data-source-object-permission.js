(function() {
  'use strict';

  var app = angular.module('radar.permissions');

  app.factory('DataSourceObjectPermission', ['session', 'hasPermissionForOrganisation', function(session, hasPermissionForOrganisation) {
    function DataSourceObjectPermission() {
    }

    DataSourceObjectPermission.prototype.hasPermission = function() {
      return true;
    };

    DataSourceObjectPermission.prototype.hasObjectPermission = function(obj) {
      if (!session.isAuthenticated) {
        return false;
      }

      var dataSource = obj.dataSource;

      if (dataSource.type !== 'RADAR') {
        return false;
      }

      var user = session.user;

      if (user.isAdmin) {
        return true;
      }

      var organisation = dataSource.organisation;

      return hasPermissionForOrganisation(user, organisation, 'EDIT_PATIENT');
    };

    return DataSourceObjectPermission;
  }]);
})();
