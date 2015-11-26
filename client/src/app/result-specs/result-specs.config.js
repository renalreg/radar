(function() {
  'use strict';

  var app = angular.module('radar.resultSpecs');

  app.config(['$stateProvider', function($stateProvider) {
    $stateProvider.state('resultSpecs', {
      url: '/results',
      templateUrl: 'app/result-specs/result-specs.html'
    });
  }]);
})();
