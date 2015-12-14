(function() {
  'use strict';

  var app = angular.module('radar.forms.fields');

  app.directive('frmWeeksAndDaysField', function() {
    return {
      restrict: 'A',
      scope: {
        required: '&',
        model: '='
      },
      templateUrl: 'app/forms/fields/weeks-and-days-field.html'
    };
  });
})();
