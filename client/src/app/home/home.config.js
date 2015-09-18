(function() {
  'use strict';

  var app = angular.module('radar.home');

  app.config(function($stateProvider) {
    $stateProvider.state('index', {
      url: '/',
      templateUrl: 'app/home/home.html'
    });
  });
})();

