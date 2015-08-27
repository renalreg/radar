(function() {
  'use strict';

  var app = angular.module('radar.auth');

  app.factory('logoutService', function(session, $state) {
    return {
      logout: logout
    };

    function logout() {
      session.logout();
      $state.go('login');
    }
  });
})();

