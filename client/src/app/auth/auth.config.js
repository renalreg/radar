(function() {
  'use strict';

  var app = angular.module('radar.auth');

  app.config(function($stateProvider) {
    $stateProvider.state('login', {
      url: '/login',
      templateUrl: 'app/auth/login.html',
      controller: 'LoginController'
    });
  });
})();

