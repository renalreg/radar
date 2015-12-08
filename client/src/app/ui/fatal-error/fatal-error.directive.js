(function() {
  'use strict';

  var app = angular.module('radar.ui.fatalError');

  app.directive('fatalError', ['$window', function($window) {
    return {
      templateUrl: 'app/ui/fatal-error/fatal-error.html',
      link: function(scope) {
        scope.open = false;

        scope.reload = function() {
          $window.location.reload();
        };

        scope.close = function() {
          scope.open = false;
        };

        scope.$on('fatalError', function() {
          scope.open = true;
        });
      }
    };
  }]);
})();
