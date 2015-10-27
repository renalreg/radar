(function() {
  'use strict';

  var app = angular.module('radar.validators');

  app.directive('equalToValidator', ['$parse', function($parse) {
    return {
      restrict: 'A',
      require: 'ngModel',
      scope: true,
      link: function(scope, element, attrs, ngModelCtrl) {
        ngModelCtrl.$parsers.push(function(confirmPassword) {
          var password = $parse(attrs.equalToValidator)(scope);
          ngModelCtrl.$setValidity('equalTo', password === confirmPassword);
          return confirmPassword;
        });
      }
    };
  }]);
})();
