(function() {
  'use strict';

  var app = angular.module('radar.permissions');

  app.factory('RadarObjectPermission', ['session', function(session) {
    function RadarObjectPermission() {
    }

    RadarObjectPermission.prototype.hasPermission = function() {
      return true;
    };

    RadarObjectPermission.prototype.hasObjectPermission = function(obj) {
      if (!session.isAuthenticated) {
        return false;
      }

      var dataSource = obj.dataSource;
      var organisation = dataSource.organisation;

      return dataSource.type === 'RADAR' && organisation.type === 'OTHER' && organisation.code === 'RADAR';
    };

    return RadarObjectPermission;
  }]);
})();
