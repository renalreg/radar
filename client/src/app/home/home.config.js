(function() {
  'use strict';

  var app = angular.module('radar.home');

  app.config(['$stateProvider', function($stateProvider) {
    $stateProvider.state('index', {
      url: '/',
      templateUrl: 'app/home/home.html',
      data: {
        public: true
      }
    });
  }]);
})();
