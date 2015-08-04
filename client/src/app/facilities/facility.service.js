(function() {
  'use strict';

  var app = angular.module('radar.facilities');

  app.factory('FacilityService', function(CurrentUserService, endpointFactory, lodash) {
    var Endpoint = endpointFactory('/facilities');

    return {
      getAvailableFacilities: getAvailableFacilities,
      getPatientFacilities: getPatientFacilities,
      getUserFacilities: getUserFacilities
    };

    function getUserFacilities() {
      return [
        {
          id: 1,
          name: 'Foo'
        }
      ];
    }

    function getPatientFacilities(patientId) {
      return [
        {
          id: 1,
          name: 'Foo'
        },
        {
          id: 2,
          name: 'Bar'
        }
      ];
    }

    function getAvailableFacilities(patientId) {
      var patientFacilities = getPatientFacilities(patientId);

      var userFacilityIds = lodash.map(getUserFacilities(), function(facility) {
        return facility.id;
      });

      return lodash.filter(patientFacilities, function(facility) {
        return userFacilityIds.indexOf(facility.id) >= 0;
      });
    }
  });
})();
