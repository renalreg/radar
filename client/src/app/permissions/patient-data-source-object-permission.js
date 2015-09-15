(function() {
  'use strict';

  var app = angular.module('radar.permissions');

  app.factory('PatientDataSourceObjectPermission', function(PermissionChain, PatientDataPermission, DataSourceObjectPermission) {
    function PatientDataSourceObjectPermission(patient) {
      PermissionChain.call(this, [
        new PatientDataPermission(patient),
        new DataSourceObjectPermission(patient)
      ]);
    }

    PatientDataSourceObjectPermission.prototype = Object.create(PermissionChain.prototype);

    return PatientDataSourceObjectPermission;
  });
})();
