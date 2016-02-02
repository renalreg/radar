(function() {
  'use strict';

  var app = angular.module('radar.auth');

  app.factory('randomPassword', ['adapter', function(adapter) {
    return function randomPassword() {
      return adapter.get('/random-password').then(function(response) {
        return response.data.password;
      });
    };
  }]);
})();
