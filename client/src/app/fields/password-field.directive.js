(function() {
  'use strict';

  var app = angular.module('radar.fields');

  app.directive('frmPasswordField', function() {
    return {
      restrict: 'A',
      scope: {
        required: '&',
        model: '='
      },
      templateUrl: 'app/fields/password-field.html'
    };
  });
})();

