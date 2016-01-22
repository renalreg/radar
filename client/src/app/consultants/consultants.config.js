(function() {
  'use strict';

  var app = angular.module('radar.consultants');

  app.config(['$stateProvider', function($stateProvider) {
    $stateProvider.state('consultants', {
      url: '/consultants',
      templateUrl: 'app/consultants/consultants.html'
    });
  }]);
})();
