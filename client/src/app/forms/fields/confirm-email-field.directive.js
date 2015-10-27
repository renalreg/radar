(function() {
  'use strict';

  var app = angular.module('radar.forms.fields');

  app.directive('frmConfirmEmailField', function() {
    return {
      restrict: 'A',
      scope: {
        required: '&',
        model: '=',
        email: '='
      },
      templateUrl: 'app/forms/fields/confirm-email-field.html'
    };
  });
})();
