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
              var state;

              if (hasPermissionForAnyGroup(session.user, 'VIEW_PATIENT')) {
                state = 'patients';
              } else {
                state = 'home';
              }

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
  }]);
})();
