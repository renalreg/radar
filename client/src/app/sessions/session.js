(function() {
  'use strict';

  var app = angular.module('radar.sessions');

  function sessionFactory(authStore, $rootScope, _) {
    function Session() {
      this.setUser(null);
      this.user = null;
      this.callbacks = {};
    }

    Session.prototype.logout = function(forced) {
      if (forced === undefined) {
        forced = false;
      }

      var userId = this.getUserId();

      // Logged in
      if (userId !== null) {
        authStore.logout();
        this.setUser(null);

        this.broadcast('logout', {
          userId: userId,
          forced: forced
        });
      }
    };

    Session.prototype.login = function(user) {
      authStore.setUserId(user.id);
      this.setUser(user);
      this.broadcast('login');
    };

    Session.prototype.getToken = function() {
      return authStore.getToken();
    };

    Session.prototype.setToken = function(token) {
      authStore.setToken(token);
      this.broadcast('refresh');
    };

    Session.prototype.getUserId = function() {
      return authStore.getUserId();
    };

    Session.prototype.setUserId = function(id) {
      return authStore.setUserId(id);
    };

    Session.prototype.getUser = function() {
      return this.user;
    };

    Session.prototype.setUser = function(user) {
      this.user = user;
      $rootScope.user = user;

      var isAuthenticated = user !== null;
      this.isAuthenticated = isAuthenticated;
      $rootScope.isAuthenticated = isAuthenticated;
    };

    Session.prototype.broadcast = function(name) {
      var self = this;

      var callbacks = self.callbacks[name] || [];
      var args = Array.prototype.slice.call(arguments, 1);

      _.forEach(callbacks, function(callback) {
        callback.apply(self, args);
      });
    };

    Session.prototype.on = function(name, callback) {
      if (this.callbacks[name] === undefined) {
        this.callbacks[name] = [];
      }

      this.callbacks[name].push(callback);
    };

    return new Session();
  }

  sessionFactory.$inject = ['authStore', '$rootScope', '_'];

  app.factory('session', sessionFactory);
})();
