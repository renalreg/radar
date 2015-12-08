(function() {
  'use strict';

  var app = angular.module('radar.auth');

  app.factory('xAuthTokenHttpInterceptor', ['session', function(session) {
    return {
      request: function(config) {
        // TODO do this on the adapter instead

        var token = session.getToken();

        if (token !== null) {
          // Send the token in the header
          config.headers['X-Auth-Token'] = token;
        }

        return config;
      },
      response: function(response) {
        // Fresh token from the server
        var token = response.headers('X-Auth-Token');

        if (token !== null) {
          // Use the fresh token for future requests
          session.setToken(token);
        }

        return response;
      }
    };
  }]);
})();
