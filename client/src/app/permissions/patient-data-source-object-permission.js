(function() {
  'use strict';

  var app = angular.module('radar.permissions');

  app.factory('PatientDataSourceObjectPermission', ['PermissionChain', 'PatientObjectPermission', 'DataSourceObjectPermission', function(PermissionChain, PatientObjectPermission, DataSourceObjectPermission) {
    function PatientDataSourceObjectPermission(patient) {
      PermissionChain.call(this, [
        new PatientObjectPermission(patient),
        new DataSourceObjectPermission(patient)
      ]);
    }

    PatientDataSourceObjectPermission.prototype = Object.create(PermissionChain.prototype);

    return PatientDataSourceObjectPermission;
  }]);
})();
