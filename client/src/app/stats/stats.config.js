(function() {
  'use strict';

  var app = angular.module('radar.stats');

  app.config(['$stateProvider', function($stateProvider) {
    $stateProvider.state('stats', {
      url: '/stats',
      templateUrl: 'app/stats/stats.html'
    });
  }]);
})();
