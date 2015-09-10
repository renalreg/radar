(function() {
  'use strict';

  var app = angular.module('radar.ui');

  app.directive('navbar', function() {
    return {
      restrict: 'A',
      scope: true,
      templateUrl: 'app/ui/navbar.html'
    };
  });
})();

