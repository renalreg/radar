(function() {
  'use strict';

  var app = angular.module('radar.form');

  app.directive('rrSelectField', function() {
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
      templateUrl: 'app/form/select-field.html'
    };
  });
})();
