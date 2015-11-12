(function() {
  'use strict';

  var app = angular.module('radar.logs');

  app.config(['$stateProvider', function($stateProvider) {
    $stateProvider.state('logs', {
      url: '/logs',
      templateUrl: 'app/logs/logs.html'
    });
  }]);
})();
