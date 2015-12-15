(function() {
  'use strict';

  var app = angular.module('radar.forms.fields');

  app.directive('frmTextareaField', function() {
    return {
      restrict: 'A',
      scope: {
        required: '&',
        model: '=',
        rows: '@'
      },
      templateUrl: 'app/forms/fields/textarea-field.html'
    };
  });
})();
