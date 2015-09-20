(function() {
  'use strict';

  var app = angular.module('radar');

  app.config(['$httpProvider', function($httpProvider) {
    $httpProvider.interceptors.push('unauthorizedHttpInterceptor');
    $httpProvider.interceptors.push('xAuthTokenHttpInterceptor');
  }]);

  app.config(['$urlRouterProvider', function($urlRouterProvider) {
    $urlRouterProvider.otherwise('/');
  }]);
})();
