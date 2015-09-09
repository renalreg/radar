(function() {
  'use strict';

  var app = angular.module('radar.fields');

  app.directive('frmTextareaField', function() {
    return {
      restrict: 'A',
      scope: {
        required: '&',
        model: '='
      },
      templateUrl: 'app/fields/textarea-field.html'
    };
  });
})();

