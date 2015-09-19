(function() {
  'use strict';

  var app = angular.module('radar.forms.fields');

  app.directive('frmDateField', function() {
    return {
      restrict: 'A',
      scope: {
        model: '=',
        required: '&',
        minDate: '=',
        maxDate: '=',
        defaultDate: '='
      },
      templateUrl: 'app/forms/fields/date-field.html'
    };
  });
})();
