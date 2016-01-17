(function() {
  'use strict';

  var app = angular.module('radar.auth');

  function directive(
    session, authService, $state, hasPermission, notificationService
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
              var state;

              if (hasPermission(session.user, 'VIEW_PATIENT')) {
                state = 'patients';
              } else {
                state = 'home';
              }

              notificationService.success('Logged in successfully.');

              $state.go(state);
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
    'session', 'authService', '$state', 'hasPermission', 'notificationService'
  ];

  app.directive('loginForm', directive);
})();
