(function() {
  'use strict';

  var app = angular.module('radar.fields');

  app.directive('frmGenderField', function() {
    return {
      restrict: 'A',
      scope: {
        required: '&',
        model: '='
      },
      templateUrl: 'app/fields/gender-field.html'
    };
  });
})();

