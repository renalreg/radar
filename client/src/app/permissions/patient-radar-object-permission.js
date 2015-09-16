(function() {
  'use strict';

  var app = angular.module('radar.permissions');

  app.factory('PatientRadarObjectPermission', function(PermissionChain, PatientDataPermission, RadarObjectPermission) {
    function PatientRadarObjectPermission(patient) {
      PermissionChain.call(this, [
        new PatientDataPermission(patient),
        new RadarObjectPermission()
      ]);
    }

    PatientRadarObjectPermission.prototype = Object.create(PermissionChain.prototype);

    return PatientRadarObjectPermission;
  });
})();
