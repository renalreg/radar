(function() {
  'use strict';

  var app = angular.module('radar.core');

  function Session(authStore) {
    this.authStore = authStore;

    this.user = null;
    this.isAuthenticated = false;
  }

  Session.prototype.logout = function() {
    this.authStore.logout();
    this.user = null;
    this.isAuthenticated = false;
  };

  Session.prototype.getToken = function() {
    return this.authStore.getToken();
  };

  Session.prototype.setToken = function(token) {
    this.authStore.setToken(token);
  };

  Session.prototype.getUserId = function() {
    return this.authStore.getUserId();
  };

  Session.prototype.setUser = function(user) {
    this.authStore.setUserId(user.id);
    this.user = user;
    this.isAuthenticated = true;
  };

  app.service('session', Session);

  app.run(function($rootScope, logoutService, session, $state) {
    $rootScope.$on('unauthorized', function() {
      session.logout();
      $state.go('login');
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
