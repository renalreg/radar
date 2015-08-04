(function() {
  'use strict';

  var app = angular.module('radar.form');

  app.directive('rrDateField', function() {
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
      templateUrl: 'app/form/date-field.html'
    };
  });
})();
