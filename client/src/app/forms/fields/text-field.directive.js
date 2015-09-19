(function() {
  'use strict';

  var app = angular.module('radar.forms.fields');

  app.directive('frmTextField', function() {
    return {
      restrict: 'A',
      scope: {
        required: '&',
        model: '='
      },
      templateUrl: 'app/forms/fields/text-field.html'
    };
  });
})();
