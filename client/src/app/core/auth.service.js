(function() {
  'use strict';

  var app = angular.module('radar.core');

  app.factory('authService', function(session, $q, store) {
    return {
      login: login
    };

    function login(username, password) {
      return store.get('users', 1).then(function(user) {
        return {
          user: user,
          token: 'TOKEN'
        };
      });
    }
  });
})();

