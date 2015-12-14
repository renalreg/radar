(function() {
  'use strict';

  var app = angular.module('radar.forms');

  app.directive('frmWeeksAndDays', function() {
    return {
      require: 'ngModel',
      transclude: true,
      template: '<div ng-transclude></div>',
      link: function(scope, element, attrs, ngModel) {
        scope.period = {
          weeks: null,
          days: null
        };

        ngModel.$render = function() {
          console.log('$render');

          var value = ngModel.$viewValue;

          if (value === null || value === undefined) {
            scope.period.weeks = null;
            scope.period.days = null;
          } else {
            scope.period.weeks = Math.floor(value / 7);
            scope.period.days = value % 7;
          }
        };

        scope.$watch('period.weeks', update);
        scope.$watch('period.days', update);

        function update() {
          var weeks = parseInt(scope.period.weeks);
          var days = parseInt(scope.period.days);
          var value;

          if (weeks >= 0 || days >= 0) {
            value = 0;

            if (weeks >= 0) {
              value += (weeks * 7);
            }

            if (days >= 0) {
              value += days;
            }

            value = value.toString();
          } else {
            value = null;
          }

          ngModel.$setViewValue(value);

          // Reset the dirty flag after initialisation
          if (value === null && (ngModel.$viewValue === undefined || ngModel.$viewValue === null)) {
            ngModel.$setPristine();
          }
        }
      }
    };
  });
})();
