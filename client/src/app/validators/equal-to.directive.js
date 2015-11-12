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
          var otherValue = $parse(attrs.equalToValidator)(scope);
          ngModelCtrl.$setValidity('equalTo', thisValue === otherValue);
          return thisValue;
        });
      }
    };
  }]);
})();