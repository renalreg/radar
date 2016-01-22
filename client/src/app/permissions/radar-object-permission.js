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

      var sourceGroup = obj.sourceGroup;
      var sourceType = obj.sourceType;

      return sourceGroup.code === 'RADAR' && sourceGroup.type === 'OTHER' && sourceType === 'RADAR';
    };

    return RadarObjectPermission;
  }]);
})();
