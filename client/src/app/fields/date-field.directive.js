(function() {
  'use strict';

  var app = angular.module('radar.fields');

  app.directive('frmDateField', function() {
    return {
      restrict: 'A',
      scope: {
        model: '=',
        required: '=',
        minDate: '=',
        maxDate: '=',
        defaultDate: '='
      },
      templateUrl: 'app/fields/date-field.html'
    };
  });
})();
