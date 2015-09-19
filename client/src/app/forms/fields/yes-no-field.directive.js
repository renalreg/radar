(function() {
  'use strict';

  var app = angular.module('radar.forms.fields');

  app.directive('frmYesNoField', function() {
    return {
      restrict: 'A',
      scope: {
        required: '&',
        model: '='
      },
      template: '<div frm-radio-field model="data.model" options="options" required="data.required"></div>',
      link: function(scope) {
        scope.data = {};

        scope.$watch(function() {
          return scope.required();
        }, function(value) {
          scope.data.required = value === true;
        });

        scope.$watch('model', function(value) {
          var viewValue;

          if (value === true) {
            viewValue = {label: 'Yes', id: true};
          } else if (value === false) {
            viewValue = {label: 'No', id: false};
          } else {
            viewValue = {label: 'Not Answered', id: null};
          }

          scope.data.model = viewValue;
        });

        scope.$watch('data.model', function(value) {
          scope.model = value.id;
        });

        scope.options = [
          {label: 'Yes', id: true},
          {label: 'No', id: false},
          {label: 'Not Answered', id: null}
        ];
      }
    };
  });
})();

