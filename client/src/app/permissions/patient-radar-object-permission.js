(function() {
  'use strict';

  var app = angular.module('radar.permissions');

  function permissionFactory(
    PermissionChain, PatientObjectPermission, RadarObjectPermission
  ) {
    function PatientRadarObjectPermission(patient) {
      PermissionChain.call(this, [
        new PatientObjectPermission(patient),
        new RadarObjectPermission()
      ]);
    }

    PatientRadarObjectPermission.prototype = Object.create(PermissionChain.prototype);

    return PatientRadarObjectPermission;
  }

  permissionFactory.$inject = [
    'PermissionChain', 'PatientObjectPermission', 'RadarObjectPermission'
  ];

  app.factory('PatientRadarObjectPermission', permissionFactory);
})();
