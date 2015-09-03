(function() {
  'use strict';

  var app = angular.module('radar.fields');

  app.directive('frmSelectField', function() {
    return {
      require: '^frmField',
      restrict: 'A',
      scope: {
        required: '=',
        model: '=',
        options: '='
      },
      templateUrl: 'app/fields/select-field.html',
      link: function(scope, element, attrs, fieldCtrl) {
        scope.$watch('required', function(value) {
          fieldCtrl.setRequired(value);
        });
      }
    };
  });
})();
