(function() {
  'use strict';

  var app = angular.module('radar.observations');

  app.config(['$stateProvider', function($stateProvider) {
    $stateProvider.state('observations', {
      url: '/observations',
      templateUrl: 'app/observations/observations.html'
    });
  }]);
})();
