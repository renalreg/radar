(function() {
  'use strict';

  var app = angular.module('radar.forms');

  // TODO validation

  app.directive('numberField', function() {
    return {
      restrict: 'A',
      scope: {
        label: '@',
        errors: '=',
        required: '=',
        model: '=',
        help: '@'
      },
      templateUrl: 'app/forms/number-field.html'
    };
  });
})();
