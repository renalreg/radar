(function() {
  'use strict';

  var app = angular.module('radar.auth');

  function AuthStore($cookies) {
    this.cookies = $cookies;
  }

  AuthStore.$inject = ['$cookies'];

  AuthStore.prototype.logout = function() {
    delete this.cookies.userId;
    delete this.cookies.token;
  };

  AuthStore.prototype.setToken = function(token) {
    this.cookies.token = token;
  };

  AuthStore.prototype.setUserId = function(userId) {
    this.cookies.userId = userId;
  };

  AuthStore.prototype.getToken = function() {
    return this.cookies.token || null;
  };

  AuthStore.prototype.getUserId = function() {
    var userId = this.cookies.userId;

    if (userId === undefined) {
      return null;
    } else {
      return parseInt(userId);
    }
  };

  app.service('authStore', AuthStore);
})();
