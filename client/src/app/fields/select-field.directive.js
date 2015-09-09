(function() {
  'use strict';

  var app = angular.module('radar.fields');

  app.directive('frmSelectField', function(unwrapSelectOption, wrapSelectOption, wrapSelectOptions) {
    return {
      restrict: 'A',
      scope: {
        required: '&',
        model: '=',
        options: '='
      },
      templateUrl: 'app/fields/select-field.html',
      link: function(scope) {
        scope.data = {};

        scope.$watch('model', function(value) {
          scope.data.model = wrapSelectOption(value);
        });

        scope.$watch('data.model', function(value) {
          scope.model = unwrapSelectOption(value);
        });

        scope.$watchCollection('options', function(options) {
          scope.data.options = wrapSelectOptions(options);
        });
      }
    };
  });
})();
