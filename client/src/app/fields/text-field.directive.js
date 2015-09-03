(function() {
  'use strict';

  var app = angular.module('radar.fields');

  app.directive('frmTextField', function() {
    return {
      require: '^frmField',
      restrict: 'A',
      scope: {
        required: '=',
        model: '='
      },
      templateUrl: 'app/fields/text-field.html',
      link: function(scope, element, attrs, fieldCtrl) {
        scope.$watch('required', function(value) {
          fieldCtrl.setRequired(value);
        });
      }
    };
  });
})();
