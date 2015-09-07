(function() {
  'use strict';

  var app = angular.module('radar.forms');

  app.directive('frmRequired', function(_, $parse) {
    return {
      require: '^frmField',
      link: function(scope, element, attrs, fieldCtrl) {
        attrs.$observe('ngRequired', function(value) {
          var required = $parse(value)(scope) === true;
          fieldCtrl.setRequired(required);
        });
      }
    };
  });
})();
