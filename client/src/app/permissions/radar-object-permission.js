(function() {
  'use strict';

  var app = angular.module('radar.permissions');

  app.factory('RadarSourceGroupObjectPermission', ['session', function(session) {
    function RadarSourceGroupObjectPermission() {
    }

    RadarSourceGroupObjectPermission.prototype.hasPermission = function() {
      return true;
    };

    RadarSourceGroupObjectPermission.prototype.hasObjectPermission = function(obj) {
      if (!session.isAuthenticated) {
        return false;
      }

      var dataSource = obj.dataSource;
      var organisation = dataSource.organisation;

      return dataSource.type === 'RADAR' && organisation.type === 'OTHER' && organisation.code === 'RADAR';
    };

    return RadarSourceGroupObjectPermission;
  }]);
})();
