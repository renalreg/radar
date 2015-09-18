(function() {
  'use strict';

  var app = angular.module('radar.auth');

  app.factory('xAuthTokenHttpInterceptor', function(session) {
    return {
      request: function(config) {
        var token = session.getToken();

        if (token !== null) {
          config.headers['X-Auth-Token'] = token;
        }

        return config;
      },
      response: function(response) {
        // Fresh token from the server
        var token = response.headers('X-Auth-Token');

        if (token !== null) {
          session.setToken(token);
        }

        return response;
      }
    };
  });
})();
