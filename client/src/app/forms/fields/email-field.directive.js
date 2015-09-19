(function() {
  'use strict';

  var app = angular.module('radar.forms.fields');

  app.directive('frmEmailField', function() {
    return {
      restrict: 'A',
      scope: {
        required: '&',
        model: '='
      },
      templateUrl: 'app/forms/fields/email-field.html'
    };
  });
})();
