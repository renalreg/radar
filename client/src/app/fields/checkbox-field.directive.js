(function() {
  'use strict';

  var app = angular.module('radar.fields');

  app.directive('frmCheckboxField', function() {
    return {
      restrict: 'A',
      scope: {
        model: '='
      },
      templateUrl: 'app/fields/checkbox-field.html'
    };
  });
})();

