(function() {
  'use strict';

  var app = angular.module('radar.permissions');

  app.factory('PatientFacilityDataPermission', function(PermissionChain, PatientDataPermission, FacilityDataPermission) {
    function PatientFacilityDataPermission(patient) {
      PermissionChain.call(this, [
        new PatientDataPermission(patient),
        new FacilityDataPermission(patient)
      ]);
    }

    PatientFacilityDataPermission.prototype = Object.create(PermissionChain.prototype);

    return PatientFacilityDataPermission;
  });
})();
