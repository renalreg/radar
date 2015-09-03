(function() {
  'use strict';

  var app = angular.module('radar.fields');

  app.directive('frmDateField', function() {
    return {
      require: '^frmField',
      restrict: 'A',
      scope: {
        model: '=',
        required: '=',
        minDate: '=',
        maxDate: '=',
        defaultDate: '='
      },
      templateUrl: 'app/fields/date-field.html',
      link: function(scope, element, attrs, fieldCtrl) {
        scope.$watch('required', function(value) {
          fieldCtrl.setRequired(value);
        });
      }
    };
  });
})();
