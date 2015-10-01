(function() {
  'use strict';

  var app = angular.module('radar.auth');

  app.factory('authService', ['session', '$q', 'store', 'adapter', function(session, $q, store, adapter) {
    return {
      login: login
    };

    function login(credentials) {
      var deferred = $q.defer();

      adapter.post('/login', {}, credentials)
        .then(function(response) {
          var userId = response.data.userId;
          var token = response.data.token;

          session.setToken(token);

          return store.findOne('users', userId)
            .then(function(user) {
              session.setUser(user);
              deferred.resolve(user);
            })
            ['catch'](function() {
              deferred.reject();
            });
        })
        ['catch'](function(response) {
          if (response.status === 422) {
            deferred.reject(response.data.errors);
          } else {
            deferred.reject();
          }
        });

      return deferred.promise;
    }
  }]);
})();

