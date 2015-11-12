(function() {
  'use strict';

  var app = angular.module('radar.validators');

  var EMAIL_REGEX = /^.+@[^\.@][^@]*\.[^\.@]+$/;

  app.directive('emailValidator', function() {
    return {
      restrict: 'A',
      require: 'ngModel',
      scope: false,
      link: function(scope, element, attrs, ngModelCtrl) {
        ngModelCtrl.$parsers.push(function(viewValue) {
          var modelValue = viewValue.trim();
          ngModelCtrl.$setValidity('email', EMAIL_REGEX.test(modelValue));
          return modelValue;
        });
      }
    };
  });
})();
