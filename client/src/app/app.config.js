(function() {
  'use strict';

  var app = angular.module('radar');

  app.config(function($stateProvider, $urlRouterProvider) {
    $urlRouterProvider.otherwise('/');
  });

  app.config(function(adapterProvider) {
    adapterProvider.setBaseUrl('http://localhost:5000');
  });
})();
