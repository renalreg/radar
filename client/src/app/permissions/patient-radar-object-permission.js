(function() {
  'use strict';

  var app = angular.module('radar.permissions');

  function permissionFactory(
    PermissionChain, PatientObjectPermission, RadarSourceGroupObjectPermission
  ) {
    function PatientRadarSourceGroupObjectPermission(patient) {
      PermissionChain.call(this, [
        new PatientObjectPermission(patient),
        new RadarSourceGroupObjectPermission()
      ]);
    }

    PatientRadarSourceGroupObjectPermission.prototype = Object.create(PermissionChain.prototype);

    return PatientRadarSourceGroupObjectPermission;
  }

  permissionFactory.$inject = [
    'PermissionChain', 'PatientObjectPermission', 'RadarSourceGroupObjectPermission'
  ];

  app.factory('PatientRadarSourceGroupObjectPermission', permissionFactory);
})();
