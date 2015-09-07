(function() {
  'use strict';

  var app = angular.module('radar.fields');

  app.directive('frmSelectField', function() {
    return {
      restrict: 'A',
      scope: {
        required: '=',
        model: '=',
        options: '='
      },
      templateUrl: 'app/fields/select-field.html'
    };
  });
})();
