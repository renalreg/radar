/* global moment */

(function() {
  'use strict';

  var app = angular.module('radar.form');

  app.directive('rrDate', function() {
    return {
      restrict: 'A',
      require: 'ngModel',
      scope: {
        minDate: '=',
        maxDate: '='
      },
      link: function(scope, element, attrs, ngModelCtrl) {
        ngModelCtrl.$parsers.push(function(viewValue) {
          var valid;
          var modelValue;

          if (viewValue === '') {
            valid = true;
            modelValue = null;
          } else if (viewValue && viewValue.length === 10) {
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
  });
})();
