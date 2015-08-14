(function() {
  'use strict';

  var app = angular.module('radar.forms');

  app.directive('dateField', function() {
    return {
      restrict: 'A',
      scope: {
        model: '=',
        label: '@',
        errors: '=',
        required: '=',
        help: '@',
        minDate: '=',
        maxDate: '=',
        defaultDate: '=',
        minDateMessage: '@',
        maxDateMessage: '@',
        requiredMessage: '@'
      },
      templateUrl: 'app/forms/date-field.html'
    };
  });
})();
