(function() {
  'use strict';

  var app = angular.module('radar.forms');

  app.directive('textField', function() {
    return {
      restrict: 'A',
      scope: {
        label: '@',
        errors: '=',
        required: '=',
        model: '=',
        help: '@'
      },
      templateUrl: 'app/forms/text-field.html'
    };
  });
})();
