(function() {
  'use strict';

  var app = angular.module('radar.forms.fields');

  app.directive('frmPasswordField', function() {
    return {
      restrict: 'A',
      scope: {
        required: '&',
        model: '='
      },
      templateUrl: 'app/forms/fields/password-field.html'
    };
  });
})();

