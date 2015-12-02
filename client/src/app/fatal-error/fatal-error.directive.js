(function() {
  'use strict';

  var app = angular.module('radar.ui');

  app.directive('fatalError', ['$window', function($window) {
    return {
      templateUrl: 'app/fatal-error/fatal-error.html',
      link: function(scope) {
        scope.reload = function() {
          $window.location.reload();
        };

        scope.close = function() {

        };
      }
    };
  }]);
})();
