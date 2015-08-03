(function () {
  'use strict';

  var app = angular.module('radar.form');

  app.directive('rrDatePicker', function() {
    return {
      restrict: 'A',
      require: 'ngModel',
      link: function(scope, element, attrs) {
        function getDate(value) {
          return value ? new Date(value) : null;
        }

        var options = {
          changeMonth: true,
          changeYear: true,
          dateFormat: 'dd/mm/yy',
          minDate: getDate(attrs.datePickerMinDate),
          maxDate: getDate(attrs.datePickerMaxDate),
          defaultDate: getDate(attrs.datePickerDefaultDate)
        };

        element.datepicker(options);

        attrs.$observe('datePickerMinDate', function() {
          element.datepicker('option', 'minDate', getDate(attrs.datePickerMinDate));
        });

        attrs.$observe('datePickerMaxDate', function() {
          element.datepicker('option', 'maxDate', getDate(attrs.datePickerMaxDate));
        });

        attrs.$observe('datePickerDefaultDate', function() {
          element.datepicker('option', 'defaultDate', getDate(attrs.datePickerDefaultDate));
        });
      }
    };
  });
})();
