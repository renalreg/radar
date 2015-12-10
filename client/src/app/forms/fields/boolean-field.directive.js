(function() {
  'use strict';

  var app = angular.module('radar.forms.fields');

  app.directive('frmBooleanField', function() {
    return {
      require: '^frmField',
      restrict: 'A',
      scope: {
        required: '&',
        model: '='
      },
      templateUrl: 'app/forms/fields/boolean-field.html',
      link: function(scope) {
        // TODO this creates two blank options when the model is null
        scope.options = [
          {
            value: undefined,
            label: ''
          },
          {
            value: true,
            label: 'Yes'
          },
          {
            value: false,
            label: 'No'
          }
        ];
      }
    };
  });
})();
