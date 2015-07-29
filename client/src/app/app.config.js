/* globals humps */

(function() {
  'use strict';

  var app = angular.module('radar');

  app.config(function(RestangularProvider) {
    RestangularProvider.setBaseUrl('http://localhost:5000');
    RestangularProvider.setRequestSuffix('/');

    RestangularProvider.addResponseInterceptor(function(data, operation) {
      if (operation === 'getList') {
        return data.data;
      } else {
        return data;
      }
    });

    RestangularProvider.addFullRequestInterceptor(function(element, operation, what, url, headers, params) {
      return {
        element: humps.decamelizeKeys(element),
        params: humps.decamelizeKeys(params)
      };
    });

    RestangularProvider.addResponseInterceptor(function(element) {
      return humps.camelizeKeys(element);
    });
  });

  app.config(function($stateProvider, $urlRouterProvider) {
    $urlRouterProvider.otherwise('/');

    $stateProvider.state('index', {
      url: '/',
      templateUrl: 'app/index.html'
    });
  });
})();
