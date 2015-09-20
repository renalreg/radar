(function() {
  'use strict';

  var app = angular.module('radar.forms.fields');

  app.directive('frmSelectField', ['unwrapSelectOption', 'wrapSelectOption', 'wrapSelectOptions', function(unwrapSelectOption, wrapSelectOption, wrapSelectOptions) {
    return {
      restrict: 'A',
      scope: {
        required: '&',
        model: '=',
        options: '='
      },
      templateUrl: 'app/forms/fields/select-field.html',
      link: function(scope) {
        scope.data = {};

        scope.$watch('model', function(value) {
          if (value === null) {
            scope.data.model = null;
          } else {
            scope.data.model = wrapSelectOption(value);
          }
        });

        scope.$watch('data.model', function(value) {
          if (value === undefined) {
            scope.model = null;
          } else {
            scope.model = unwrapSelectOption(value);
          }
        });

        scope.$watchCollection('options', function(options) {
          scope.data.options = wrapSelectOptions(options);
        });
      }
    };
  }]);
})();
