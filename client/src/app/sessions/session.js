(function() {
  'use strict';

  var app = angular.module('radar.sessions');

  function sessionFactory(authStore, $rootScope) {
    function Session() {
      this.setUser(null);
    }

    Session.prototype.logout = function() {
      authStore.logout();
      this.setUser(null);
      $rootScope.$broadcast('sessions.logout');
    };

    Session.prototype.login = function(user) {
      authStore.setUserId(user.id);
      this.setUser(user);
      $rootScope.$broadcast('sessions.login');
    };

    Session.prototype.getToken = function() {
      return authStore.getToken();
    };

    Session.prototype.setToken = function(token) {
      authStore.setToken(token);
      $rootScope.$broadcast('sessions.refresh');
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

    return new Session();
  }

  sessionFactory.$inject = ['authStore', '$rootScope'];

  app.factory('session', sessionFactory);

  app.run(['$rootScope', 'authService', '$state', function($rootScope, authService, $state) {
    $rootScope.$on('unauthorized', function() {
      authService.logout();
      $state.go('login');
    });
  }]);
})();
