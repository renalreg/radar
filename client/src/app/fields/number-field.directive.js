(function() {
  'use strict';

  var app = angular.module('radar.fields');

  // TODO validators

  app.directive('frmNumberField', function() {
    return {
      restrict: 'A',
      scope: {
        required: '=',
        model: '='
      },
      templateUrl: 'app/fields/number-field.html'
    };
  });
})();
