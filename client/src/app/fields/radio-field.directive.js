(function() {
  'use strict';

  var app = angular.module('radar.fields');

  app.directive('frmRadioField', function(wrapRadioOptions, toRadioView, toRadioModel) {
    return {
      restrict: 'A',
      scope: {
        model: '=',
        required: '&',
        options: '='
      },
      templateUrl: 'app/fields/radio-field.html',
      link: function(scope) {
        // Note: ng-repeat creates a child scope which breaks ng-model="model". The model variable is a primitive type
        // (i.e. not an object) so when the value is updated in the child scope it won't be updated in the parent scope
        // (see prototypical inheritance). So we create an object (data) in this scope and bind to a property on that
        // instead. We then create a two-way binding using scope.$watch between "model" and "data.model". The other
        // scope properties are okay as they aren't updated in the child scope (the child scope defers to the parent
        // scope).

        scope.data = {};

        scope.$watch('model', function(value) {
          scope.data.model = toRadioView(value);
        });

        scope.$watch('data.model', function(value) {
          scope.model = toRadioModel(scope.options, value);
        });

        scope.$watchCollection('options', function(options) {
          scope.data.options = wrapRadioOptions(options);
        });
      }
    };
  });
})();
