(function() {
  'use strict';

  var app = angular.module('radar.facilities');

  app.directive('rrFacilityField', function(FacilityService) {
    return {
      restrict: 'A',
      scope: {
        patient: '=',
        model: '=',
        required: '='
      },
      templateUrl: 'app/facilities/facility-field.html',
      link: function(scope) {
        scope.facilities = FacilityService.getAvailableFacilities(scope.patient.id);

        if (!scope.model) {
          scope.model = scope.facilities[0];
        }
      }
    };
  });
})();
