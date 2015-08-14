(function() {
  'use strict';

  var app = angular.module('radar.facilities');

  app.directive('facilityField', function(store) {
    return {
      restrict: 'A',
      scope: {
        patient: '=',
        model: '=',
        required: '='
      },
      templateUrl: 'app/facilities/facility-field.html',
      link: function(scope) {
        store.query('facilities').then(function(facilities) {
          scope.facilities = facilities;

          if (!scope.model) {
            scope.model = scope.facilities[0];
          }
        });
      }
    };
  });
})();
