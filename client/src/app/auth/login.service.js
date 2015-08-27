(function() {
  'use strict';

  var app = angular.module('radar.auth');

  app.factory('loginService', function(session, authService) {
    return {
      login: login
    };

    function login(username, password) {
      return authService.login(username, password).then(function(response) {
        session.login(response.user, response.token);
        return response.user;
      });
    }
  });
})();
