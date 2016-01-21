(function() {
  'use strict';

  var app = angular.module('radar.store');

  function tokenRequestFactory(session) {
    return function(config) {
      var token = session.getToken();

      if (token !== null) {
        if (config.headers === undefined) {
          config.headers = {};
        }

        // Send the token in the header
        config.headers['X-Auth-Token'] = token;
      }

      return config;
    };
  }

  tokenRequestFactory.$inject = [
    'session'
  ];

  app.factory('tokenRequest', tokenRequestFactory);

  app.config(['adapterProvider', function(adapterProvider) {
    adapterProvider.beforeRequest('tokenRequest');
  }]);
})();
