(function() {
  'use strict';

  var app = angular.module('radar.fields');

  app.directive('frmYesNoField', function() {
    return {
      restrict: 'A',
      scope: {
        required: '&',
        model: '='
      },
      template: '<div frm-radio-field model="model" options="options" required="data.required"></div>',
      link: function(scope) {
        scope.data = {};

        scope.$watch(function() {
          return scope.required();
        }, function(value) {
          scope.data.required = value === true;
        });

        scope.options = [
          {
            label: 'Yes',
            id: true
          },
          {
            label: 'No',
            id: false
          },
          {
            label: 'Not Answered',
            id: null
          }
        ];
      }
    };
  });
})();

