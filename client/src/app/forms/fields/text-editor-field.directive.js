(function() {
  'use strict';

  var app = angular.module('radar.forms.fields');

  app.directive('frmTextEditorField', function() {
    return {
      restrict: 'A',
      scope: {
        required: '&',
        model: '='
      },
      templateUrl: 'app/forms/fields/text-editor-field.html'
    };
  });
})();
