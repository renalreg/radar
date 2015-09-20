(function() {
  'use strict';

  var app = angular.module('radar.permissions');

  app.factory('PatientRadarObjectPermission', ['PermissionChain', 'PatientObjectPermission', 'RadarObjectPermission', function(PermissionChain, PatientObjectPermission, RadarObjectPermission) {
    function PatientRadarObjectPermission(patient) {
      PermissionChain.call(this, [
        new PatientObjectPermission(patient),
        new RadarObjectPermission()
      ]);
    }

    PatientRadarObjectPermission.prototype = Object.create(PermissionChain.prototype);

    return PatientRadarObjectPermission;
  }]);
})();
