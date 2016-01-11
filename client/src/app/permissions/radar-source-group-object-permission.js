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

      var sourceGroup = obj.sourceGroup;
      var sourceType = obj.sourceType;

      return sourceGroup.code === 'RADAR' && sourceGroup.type === 'OTHER' && sourceType.id === 'RADAR';
    };

    return RadarSourceGroupObjectPermission;
  }]);
})();
