(function () {
  'use strict';

  var app = angular.module('radar');

  app.factory('FacilityService', function() {
    return {
      getFacilitiesForPatient: getFacilitiesForPatient
    };

    function getFacilitiesForPatient(patientId) {
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
  });
})();
