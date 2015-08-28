(function() {
  'use strict';

  var app = angular.module('radar.auth');

  function AuthStore($cookies) {
    this.cookies = $cookies;
  }

  AuthStore.prototype.login = function(userId, token) {
    this.cookies.userId = userId;
    this.cookies.token = token;
  };

  AuthStore.prototype.logout = function() {
    delete this.cookies.userId;
    delete this.cookies.token;
  };

  AuthStore.prototype.getUserId = function() {
    var userId = this.cookies.userId;

    if (userId === undefined) {
      return null;
    } else {
      return parseInt(userId);
    }
  };

  AuthStore.prototype.getToken = function() {
    return this.cookies.token || null;
  };

  app.service('authStore', AuthStore);
})();
