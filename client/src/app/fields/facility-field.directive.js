(function() {
  'use strict';

  var app = angular.module('radar.fields');

  app.directive('frmFacilityField', function(store, session, _) {
    return {
      restrict: 'A',
      scope: {
        model: '=',
        required: '&'
      },
      templateUrl: 'app/fields/facility-field.html',
      link: function(scope) {
        store.findMany('facilities', {isInternal: true}).then(function(facilities) {
          scope.facilities = facilities;
        });
      }
    };
  });
})();

