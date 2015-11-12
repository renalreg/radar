(function() {
  'use strict';

  var app = angular.module('radar.validators');

  var INTEGER_REGEX = /^[+-]?[0-9]+$/;

  app.directive('integerValidator', function() {
    return {
    restrict: 'A',
    require: 'ngModel',
    scope: false,
    link: function(scope, element, attrs, ngModelCtrl) {
      ngModelCtrl.$parsers.push(function(viewValue) {
        var modelValue;
        var valid;

        if (viewValue === undefined || viewValue === null) {
          modelValue = null;
          valid = true;
        } else {
          modelValue = viewValue.trim();

          if (modelValue.length === 0) {
            modelValue = null;
            valid = true;
          } else if (INTEGER_REGEX.test(modelValue)) {
            modelValue = parseInt(modelValue, 10);
            valid = true;
          } else {
            modelValue = null;
            valid = false;
          }
        }

        ngModelCtrl.$setValidity('integer', valid);

        return modelValue;
      });
    }
  };
  });
})();
