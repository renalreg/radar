(function() {
  'use strict';

  var app = angular.module('radar.forms.fields');

  app.directive('frmSelectField', ['toSelectModel', 'toSelectView', 'wrapSelectOptions', function(toSelectModel, toSelectView, wrapSelectOptions) {
    return {
      restrict: 'A',
      scope: {
        required: '&',
        model: '=',
        options: '=',
        optionsId: '@',
        optionsLabel: '@',
      },
      templateUrl: 'app/forms/fields/select-field.html',
      link: function(scope) {
        scope.data = {};

        scope.$watch('model', function(value) {
          scope.data.model = toSelectView(value, scope.optionsId, scope.optionsLabel);
        });

        scope.$watch('data.model', function(value) {
          scope.model = toSelectModel(value);
        });

        scope.$watchCollection('options', function(options) {
          scope.data.options = wrapSelectOptions(options, scope.optionsId, scope.optionsLabel);
        });
      }
    };
  }]);
})();
