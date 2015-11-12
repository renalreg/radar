(function() {
  'use strict';

  var app = angular.module('radar.validators');

  app.directive('equalToValidator', ['$parse', function($parse) {
    return {
      restrict: 'A',
      require: 'ngModel',
      scope: false,
      link: function(scope, element, attrs, ngModelCtrl) {
        ngModelCtrl.$parsers.push(function(thisValue) {
          var otherValue = getOtherValue();
          validate(thisValue, otherValue);
          return thisValue;
        });

        scope.$watch(function() {
          return getOtherValue();
        }, function(otherValue) {
          var thisValue = getThisValue();
          validate(thisValue, otherValue);
        });

        function getThisValue() {
          return ngModelCtrl.$modelValue;
        }

        function getOtherValue() {
          return $parse(attrs.equalToValidator)(scope);
        }

        function validate(thisValue, otherValue) {
          var valid = thisValue === otherValue;
          ngModelCtrl.$setValidity('equalTo', valid);
          return valid;
        }
      }
    };
  }]);
})();
