(function() {
  'use strict';

  var app = angular.module('radar.ui');

  app.directive('tick', function() {
    return {
      restrict: 'A',
      scope: {
        tick: '='
      },
      templateUrl: 'app/ui/tick.html',
      link: function(scope) {
        scope.isTrue = function() {
          return scope.tick === true;
        };

        scope.isFalse = function() {
          return scope.tick === false;
        };

        scope.isNeither = function() {
          return !scope.isTrue() && !scope.isFalse();
        };
      }
    };
  });
})();

