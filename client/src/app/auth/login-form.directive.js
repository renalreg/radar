(function() {
  'use strict';

  var app = angular.module('radar.auth');

  app.directive('loginForm', ['session', 'loginService', '$state', function(session, loginService, $state) {
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

          return loginService.login(credentials)
            .then(function() {
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
