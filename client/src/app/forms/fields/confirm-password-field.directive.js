(function() {
  'use strict';

  var app = angular.module('radar.forms.fields');

  app.directive('frmConfirmPasswordField', function() {
    return {
      restrict: 'A',
      scope: {
        required: '&',
        model: '=',
        password: '='
      },
      templateUrl: 'app/forms/fields/confirm-password-field.html'
    };
  });
})();
