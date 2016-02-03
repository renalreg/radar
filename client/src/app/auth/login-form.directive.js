(function() {
  'use strict';

  var app = angular.module('radar.auth');

  function directive(
    session, authService, notificationService, loginRedirect
  ) {
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
              notificationService.success('Logged in successfully.');
              loginRedirect(session.user);
            })
            ['catch'](function(errors) {
              if (errors) {
                scope.errors = errors;
              }
            });
        };
      }
    };
  }

  directive.$inject = [
    'session', 'authService', 'notificationService', 'loginRedirect'
  ];

  app.directive('loginForm', directive);
})();
