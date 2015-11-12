(function() {
  'use strict';

  var app = angular.module('radar.validators');

  var DATE_REGEX = /^[0-9]{2}\/[0-9]{2}\/[0-9]{4}$/;

  app.directive('dateValidator', ['moment', function(moment) {
    return {
      restrict: 'A',
      require: 'ngModel',
      // TODO don't use scope
      scope: {
        minDate: '=',
        maxDate: '='
      },
      link: function(scope, element, attrs, ngModelCtrl) {
        ngModelCtrl.$parsers.push(function(viewValue) {
          var valid;
          var modelValue;

          if (viewValue === null || viewValue === undefined) {
            valid = true;
            modelValue = null;
          } else {
            modelValue = viewValue.trim();

            if (DATE_REGEX.test(modelValue)) {
              var date = moment(viewValue, 'DD/MM/YYYY');

              if (date.isValid()) {
                valid = true;
                modelValue = date.format('YYYY-MM-DD');
              } else {
                valid = false;
                modelValue = null;
              }
            } else {
              valid = false;
              modelValue = null;
            }
          }

          ngModelCtrl.$setValidity('date', valid);

          if (scope.minDate && modelValue && moment(modelValue) < moment(scope.minDate)) {
            ngModelCtrl.$setValidity('minDate', false);
            modelValue = null;
          } else {
            ngModelCtrl.$setValidity('maxDate', true);
          }

          if (scope.maxDate && modelValue && moment(modelValue) > moment(scope.maxDate)) {
            ngModelCtrl.$setValidity('maxDate', false);
            modelValue = null;
          } else {
            ngModelCtrl.$setValidity('maxDate', true);
          }

          return modelValue;
        });

        ngModelCtrl.$formatters.push(function(value) {
          if (value) {
            return moment(value).format('DD/MM/YYYY');
          } else {
            return '';
          }
        });
      }
    };
  }]);
})();
