(function() {
  'use strict';

  var app = angular.module('radar.fields');

  app.directive('frmEmailField', function() {
    return {
      restrict: 'A',
      scope: {
        required: '&',
        model: '='
      },
      templateUrl: 'app/fields/email-field.html'
    };
  });
})();
