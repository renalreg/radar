(function() {
  'use strict';

  var app = angular.module('radar.auth');

  app.directive('logout', ['logoutService', '$state', function(logoutService, $state) {
    return {
      restrict: 'A',
      link: function(scope, element) {
        element.on('click', function() {
          scope.$apply(function() {
            logoutService.logout();
            $state.go('login');
          });
        });
      }
    };
  }]);
})();
