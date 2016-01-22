(function() {
  'use strict';

  var app = angular.module('radar.store');

  function tokenResponseFactory(session) {
    return function(promise) {
      return promise.then(function(response) {
        // Fresh token from the server
        var token = response.headers('X-Auth-Token');

        if (token !== null) {
          // Use the fresh token for future requests
          session.setToken(token);
        }

        return response;
      });
    };
  }

  tokenResponseFactory.$inject = [
    'session'
  ];

  app.factory('tokenResponse', tokenResponseFactory);

  app.config(['adapterProvider', function(adapterProvider) {
    adapterProvider.afterResponse('tokenResponse');
  }]);
})();
