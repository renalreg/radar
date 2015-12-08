(function() {
  'use strict';

  var app = angular.module('radar.auth');

  app.directive('logout', ['authService', '$state', function(authService, $state) {
    return {
      restrict: 'A',
      link: function(scope, element) {
        element.on('click', function() {
          scope.$apply(function() {
            authService.logout();
            $state.go('login');
          });
        });
      }
    };
  }]);
})();
