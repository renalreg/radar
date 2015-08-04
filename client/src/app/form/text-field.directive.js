(function() {
  'use strict';

  var app = angular.module('radar.form');

  app.directive('rrTextField', function() {
    return {
      restrict: 'A',
      scope: {
        label: '@',
        errors: '=',
        required: '=',
        model: '=',
        help: '@'
      },
      templateUrl: 'app/form/text-field.html'
    };
  });
})();
