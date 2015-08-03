(function() {
  'use strict';

  var app = angular.module('radar.core');

  app.config(function($stateProvider) {
    $stateProvider.state('index', {
      url: '/',
      templateUrl: 'app/core/index.html'
    });

    $stateProvider.state('login', {
      url: '/login',
      templateUrl: 'app/core/login.html'
    });
  });
})();
