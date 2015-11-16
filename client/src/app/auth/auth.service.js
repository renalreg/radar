(function() {
  'use strict';

  var app = angular.module('radar.auth');

  app.factory('authService', ['session', '$q', 'store', 'adapter', function(session, $q, store, adapter) {
    return {
      login: login,
      forgotUsername: forgotUsername,
      forgotPassword: forgotPassword,
      resetPassword: resetPassword
    };

    function errorHandler(promise) {
      if (promise === undefined) {
        promise = $q;
      }

      return function(response) {
        if (response.status === 422) {
          return promise.reject(response.data.errors);
        } else {
          return promise.reject();
        }
      };
    }

    function login(credentials) {
      var deferred = $q.defer();

      adapter.post('/login', {}, credentials)
        .then(function(response) {
          var userId = response.data.userId;
          var token = response.data.token;

          session.setToken(token);

          return store.findOne('users', userId)
            .then(function(user) {
              session.login(user);
              deferred.resolve(user);
            })
            ['catch'](function() {
              deferred.reject();
            });
        })
        ['catch'](errorHandler(deferred));

      return deferred.promise;
    }

    function forgotUsername(email) {
      return adapter.post('/forgot-username', {}, {email: email})['catch'](errorHandler());
    }

    function forgotPassword(username) {
      return adapter.post('/forgot-password', {}, {username: username})['catch'](errorHandler());
    }

    function resetPassword(token, username, password) {
      var data = {
        token: token,
        username: username,
        password: password
      };

      return adapter.post('/reset-password', {}, data)['catch'](errorHandler());
    }
  }]);
})();
