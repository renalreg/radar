(function() {
  'use strict';

  var app = angular.module('radar.fields');

  // TODO validators

  app.directive('frmIntegerField', function() {
    return {
      restrict: 'A',
      scope: {
        required: '=',
        model: '='
      },
      templateUrl: 'app/fields/integer-field.html'
    };
  });
})();
