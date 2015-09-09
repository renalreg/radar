(function() {
  'use strict';

  var app = angular.module('radar.permissions');

  app.factory('FacilityDataPermission', function(session, _) {
    function FacilityDataPermission() {
    }

    FacilityDataPermission.prototype.hasPermission = function() {
      return true;
    };

    FacilityDataPermission.prototype.hasObjectPermission = function(obj) {
      if (!session.isAuthenticated) {
        return false;
      }

      var objFacility = obj.facility;

      if (!objFacility.isInternal) {
        return false;
      }

      var objUnit = objFacility.unit;

      if (!objUnit) {
        return false;
      }

      if (session.user.isAdmin) {
        return true;
      }

      var userUnits = session.user.units;

      for (var i = 0; i < userUnits.length; i++) {
        var userUnit = userUnits[i];

        if (userUnit.unit.id === objUnit.id) {
          return userUnit.hasEditPatientPermission;
        }
      }

      return false;
    };

    return FacilityDataPermission;
  });
})();

