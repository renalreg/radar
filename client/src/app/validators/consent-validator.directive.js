(function() {
  'use strict';

  var app = angular.module('radar.validators');

  app.directive('consentValidator', function() {
    return {
      restrict: 'A',
      require: 'ngModel',
      link: function(scope, element, attrs, ngModelCtrl) {
        ngModelCtrl.$setValidity('consent', ngModelCtrl.$viewValue);

        ngModelCtrl.$parsers.push(function(viewValue) {
          ngModelCtrl.$setValidity('consent', viewValue);
          return viewValue;
        });
      }
    };
  });
})();
