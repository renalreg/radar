(function() {
  'use strict';

  var app = angular.module('radar.fields');

  app.directive('frmTextField', function() {
    return {
      restrict: 'A',
      scope: {
        required: '&',
        model: '='
      },
      templateUrl: 'app/fields/text-field.html'
    };
  });
})();
