(function() {
  'use strict';

  var app = angular.module('radar.forms.fields');

  app.directive('frmCheckboxField', function() {
    return {
      restrict: 'A',
      scope: {
        model: '='
      },
      transclude: true,
      templateUrl: 'app/forms/fields/checkbox-field.html'
    };
  });
})();
