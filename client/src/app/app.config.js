(function() {
  'use strict';

  var app = angular.module('radar');

  app.config(function($stateProvider, $urlRouterProvider) {
    $urlRouterProvider.otherwise('/');
  });
})();
