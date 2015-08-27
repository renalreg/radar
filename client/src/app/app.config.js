(function() {
  'use strict';

  var app = angular.module('radar');

  app.config(function($httpProvider) {
    $httpProvider.interceptors.push('unauthorizedHttpInterceptor');
    $httpProvider.interceptors.push('xAuthTokenHttpInterceptor');
  });

  app.config(function($stateProvider, $urlRouterProvider) {
    $urlRouterProvider.otherwise('/');
  });

  app.config(function(adapterProvider) {
    adapterProvider.setBaseUrl('http://localhost:5000');
  });

  app.config(function($stateProvider) {
    $stateProvider.state('index', {
      url: '/',
      templateUrl: 'app/core/index.html'
    });
  });
})();
