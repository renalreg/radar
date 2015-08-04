(function() {
  'use strict';

  var app = angular.module('radar.form');

  // TODO validation

  app.directive('rrNumberField', function() {
    return {
      restrict: 'A',
      scope: {
        label: '@',
        errors: '=',
        required: '=',
        model: '=',
        help: '@'
      },
      templateUrl: 'app/form/number-field.html'
    };
  });
})();


