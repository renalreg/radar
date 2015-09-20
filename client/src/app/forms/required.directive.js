(function() {
  'use strict';

  var app = angular.module('radar.forms');

  app.directive('frmRequired', ['$parse', function($parse) {
    return {
      require: '^frmField',
      link: function(scope, element, attrs, fieldCtrl) {
        var requiredGetter = null;

        attrs.$observe('ngRequired', function(value) {
          requiredGetter = $parse(value);
        });

        scope.$watch(function() {
          return requiredGetter !== null && requiredGetter(scope) === true;
        }, function(value) {
          fieldCtrl.setRequired(value);
        });
      }
    };
  }]);
})();
