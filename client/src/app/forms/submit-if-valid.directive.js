(function() {
  'use strict';

  var app = angular.module('radar.forms');

  app.directive('submitIfValid', function() {
    return {
      require: '^form',
      scope: {
        submit: '&submitIfValid'
      },
      link: function(scope, element, attrs, formCtrl) {
        element.on('submit', function(event) {
          event.preventDefault();

          if (formCtrl.$valid) {
            scope.submit();
          }
        });
      }
    };
  });
})();

