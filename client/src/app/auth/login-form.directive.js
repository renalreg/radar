(function() {
  'use strict';

  var app = angular.module('radar.auth');

  app.directive('loginForm', function(session, loginService, $state) {
    return {
      restrict: 'A',
      scope: {},
      templateUrl: 'app/auth/login-form.html',
      link: function(scope) {
        var credentials = {
          username: '',
          password: ''
        };

        scope.credentials = credentials;

        scope.errors = {};

        scope.login = function() {
          scope.errors = {};

          loginService.login(credentials.username, credentials.password)
            .then(function() {
              $state.go('patients');
            })
            .catch(function(errors) {
              if (errors) {
                scope.errors = errors;
              }
            });
        };

        scope.logout = function() {
          session.logout();
        };
      }
    };
  });
})();
