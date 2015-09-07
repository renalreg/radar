(function() {
  'use strict';

  var app = angular.module('radar.fields');

  app.directive('frmPasswordField', function() {
    return {
      require: '^frmField',
      restrict: 'A',
      scope: {
        required: '=',
        model: '='
      },
      templateUrl: 'app/fields/password-field.html',
      link: function(scope, element, attrs, fieldCtrl) {
        scope.$watch('required', function(value) {
          fieldCtrl.setRequired(value);
        });
      }
    };
  });
})();

