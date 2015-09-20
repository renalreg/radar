(function() {
  'use strict';

  var app = angular.module('radar.permissions');

  app.factory('DataSourceObjectPermission', ['session', function(session) {
    function DataSourceObjectPermission() {
    }

    DataSourceObjectPermission.prototype.hasPermission = function() {
      return true;
    };

    DataSourceObjectPermission.prototype.hasObjectPermission = function(obj) {
      if (!session.isAuthenticated) {
        return false;
      }

      var objDataSource = obj.dataSource;

      if (objDataSource.type !== 'RADAR') {
        return false;
      }

      if (session.user.isAdmin) {
        return true;
      }

      var objOrganisation = objDataSource.organisation;
      var userOrganisations = session.user.organisations;

      for (var i = 0; i < userOrganisations.length; i++) {
        var userOrganisation = userOrganisations[i];

        if (userOrganisation.organisation.id === objOrganisation.id) {
          return userOrganisation.hasEditPatientPermission;
        }
      }

      return false;
    };

    return DataSourceObjectPermission;
  }]);
})();

