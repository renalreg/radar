(function() {
  'use strict';

  var app = angular.module('radar');

  app.config(['$urlRouterProvider', function($urlRouterProvider) {
    $urlRouterProvider.otherwise('/');
  }]);
})();
