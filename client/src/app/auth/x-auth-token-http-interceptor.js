(function() {
  'use strict';

  var app = angular.module('radar.auth');

  app.factory('xAuthTokenHttpInterceptor', function(session) {
    return {
      request: function(config) {
        var token = session.getToken();

        if (token !== null) {
          config.headers['X-AUTH-TOKEN'] = token;
        }

        return config;
      }
    };
  });
})();
