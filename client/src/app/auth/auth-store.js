(function() {
  'use strict';

  var app = angular.module('radar.auth');

  /** Service for storing user credentials (e.g tokens) */
  function authStore(localStorageService) {
    return {
      logout: logout,
      setToken: setToken,
      setUserId: setUserId,
      getToken: getToken,
      getUserId: getUserId
    };

    function logout() {
      localStorageService.remove('userId');
      localStorageService.remove('token');
    }

    function setToken(token) {
      localStorageService.set('token', token);
    }

    function setUserId(userId) {
      localStorageService.set('userId', userId);
    }

    function getToken() {
      return localStorageService.get('token');
    }

    function getUserId() {
      var userId = localStorageService.get('userId');

      if (userId) {
        userId = parseInt(userId);
      }

      return userId;
    }
  }

  authStore.$inject = ['localStorageService'];

  app.factory('authStore', authStore);
})();
