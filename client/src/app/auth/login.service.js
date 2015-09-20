(function() {
  'use strict';

  var app = angular.module('radar.auth');

  app.factory('loginService', ['session', 'authService', function(session, authService) {
    return {
      login: login
    };

    function login(credentials) {
      return authService.login(credentials);
    }
  }]);
})();
