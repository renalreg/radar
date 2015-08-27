(function() {
  'use strict';

  var app = angular.module('radar.auth');

  app.directive('logout', function(logoutService) {
    return {
      restrict: 'A',
      link: function(scope, element) {
        element.on('click', function() {
          scope.$apply(function() {
            logoutService.logout();
          });
        });
      }
    };
  });
})();


