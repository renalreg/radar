(function () {
  'use strict';

  var app = angular.module('radar');

  app.directive('rrFacilityField', function(FacilityService) {
    return {
      restrict: 'A',
      scope: {
        patient: '=',
        model: '=',
        required: '='
      },
      templateUrl: 'app/facility/facility-field.html',
      link: function(scope) {
        scope.facilities = FacilityService.getFacilitiesForPatient(scope.patient.id);

        if (!scope.model) {
          scope.model = scope.facilities[0];
        }
      }
    };
  });
})();
