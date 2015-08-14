(function() {
  'use strict';

  var app = angular.module('radar.forms');

  app.directive('selectField', function() {
    return {
      restrict: 'A',
      scope: {
        label: '@',
        errors: '=',
        required: '=',
        model: '=',
        options: '=',
        help: '@'
      },
      templateUrl: 'app/forms/select-field.html'
    };
  });
})();
