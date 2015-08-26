(function() {
  'use strict';

  var app = angular.module('radar.login');

  app.config(function($stateProvider) {
    $stateProvider.state('login', {
      url: '/login',
      templateUrl: 'app/login/login.html',
      controller: 'LoginController'
    });
  });
})();

