(function() {
  'use strict';

  var app = angular.module('radar.auth');

  app.directive('loginForm', ['session', 'authService', '$state', function(session, authService, $state) {
    return {
      restrict: 'A',
      scope: {},
      templateUrl: 'app/auth/login-form.html',
      link: function(scope) {
        var credentials = {
          username: '',
          password: '',
          logoutOtherSessions: false
        };

        scope.credentials = credentials;

        scope.errors = {};

        scope.login = function() {
          scope.errors = {};

          return authService.login(credentials)
            .then(function() {
              // Redirect to the patients list
              // TODO not all users will have access to this
              $state.go('patients');
            })
            ['catch'](function(errors) {
              if (errors) {
                scope.errors = errors;
              }
            });
        };
      }
    };
  }]);
})();
