(function() {
  'use strict';

  var app = angular.module('radar.permissions');

  function permissionFactory(
    PermissionChain, PatientObjectPermission, SourceGroupObjectPermission
  ) {
    function PatientSourceGroupObjectPermission(patient) {
      PermissionChain.call(this, [
        new PatientObjectPermission(patient),
        new SourceGroupObjectPermission(patient)
      ]);
    }

    PatientSourceGroupObjectPermission.prototype = Object.create(PermissionChain.prototype);

    return PatientSourceGroupObjectPermission;
  }

  permissionFactory.$inject = [
    'PermissionChain', 'PatientObjectPermission', 'SourceGroupObjectPermission'
  ];

  app.factory('PatientSourceGroupObjectPermission', permissionFactory);
})();
