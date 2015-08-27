(function() {
  'use strict';

  var app = angular.module('radar.core');

  function Session(authStore) {
    this.authStore = authStore;

    this.user = null;
    this.isAuthenticated = false;
  }

  Session.prototype.login = function(user, token) {
    this.authStore.login(user.id, token);
    this.setUser(user);
  };

  Session.prototype.logout = function() {
    this.authStore.logout();
    this.setUser(null);
  };

  Session.prototype.getToken = function() {
    return this.authStore.getToken();
  };

  Session.prototype.getUserId = function() {
    return this.authStore.getUserId();
  };

  Session.prototype.setUser = function(user) {
    this.user = user;
    this.isAuthenticated = user !== null;
  };

  app.service('session', Session);

  app.run(function($rootScope, logoutService, session) {
    $rootScope.$on('unauthorized', function() {
      logoutService.logout();
    });

    $rootScope.$watch(function() {
      return session.user;
    }, function(user) {
      $rootScope.user = user;
    });

    $rootScope.$watch(function() {
      return session.isAuthenticated;
    }, function(isAuthenticated) {
      $rootScope.isAuthenticated = isAuthenticated;
    });
  });
})();

