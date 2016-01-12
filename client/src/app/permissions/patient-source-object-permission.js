(function() {
  'use strict';

  var app = angular.module('radar.permissions');

  function permissionFactory(
    PermissionChain, PatientObjectPermission, SourceObjectPermission
  ) {
    function PatientSourceObjectPermission(patient) {
      PermissionChain.call(this, [
        new PatientObjectPermission(patient),
        new SourceObjectPermission(patient)
      ]);
    }

    PatientSourceObjectPermission.prototype = Object.create(PermissionChain.prototype);

    return PatientSourceObjectPermission;
  }

  permissionFactory.$inject = [
    'PermissionChain', 'PatientObjectPermission', 'SourceObjectPermission'
  ];

  app.factory('PatientSourceObjectPermission', permissionFactory);
})();
