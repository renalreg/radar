(function() {
  'use strict';

  var app = angular.module('radar.fields');

  app.directive('frmBooleanField', function() {
    return {
      require: '^frmField',
      restrict: 'A',
      scope: {
        required: '=',
        model: '='
      },
      templateUrl: 'app/fields/boolean-field.html',
      link: function(scope, element, attrs, fieldCtrl) {
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

        scope.$watch('required', function(value) {
          fieldCtrl.setRequired(value);
        });
      }
    };
  });
})();
