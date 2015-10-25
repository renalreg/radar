(function() {
  'use strict';

  var app = angular.module('radar.permissions');

  function permissionFactory(
    PermissionChain, PatientObjectPermission, DataSourceObjectPermission
  ) {
    function PatientDataSourceObjectPermission(patient) {
      PermissionChain.call(this, [
        new PatientObjectPermission(patient),
        new DataSourceObjectPermission(patient)
      ]);
    }

    PatientDataSourceObjectPermission.prototype = Object.create(PermissionChain.prototype);

    return PatientDataSourceObjectPermission;
  }

  permissionFactory.$inject = [
    'PermissionChain', 'PatientObjectPermission', 'DataSourceObjectPermission'
  ];

  app.factory('PatientDataSourceObjectPermission', permissionFactory);
})();
