(function() {
  'use strict';

  var app = angular.module('radar.auth');

  app.factory('logoutService', function(session, adapter) {
    return {
      logout: logout
    };

    function logout() {
      adapter.post('/logout').finally(function() {
        session.logout();
      });
    }
  });
})();
