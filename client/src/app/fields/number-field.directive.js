(function() {
  'use strict';

  var app = angular.module('radar.fields');

  // TODO validation

  app.directive('frmNumberField', function() {
    return {
      require: '^frmField',
      restrict: 'A',
      scope: {
        required: '=',
        model: '='
      },
      templateUrl: 'app/fields/number-field.html',
      link: function(scope, element, attrs, fieldCtrl) {
        scope.$watch('required', function(value) {
          fieldCtrl.setRequired(value);
        });
      }
    };
  });
})();
