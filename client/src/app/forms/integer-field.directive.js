(function() {
  'use strict';

  var app = angular.module('radar.forms');

  // TODO validation

  app.directive('integerField', function() {
    return {
      restrict: 'A',
      scope: {
        label: '@',
        errors: '=',
        required: '=',
        model: '=',
        help: '@'
      },
      templateUrl: 'app/forms/integer-field.html'
    };
  });
})();

