(function() {
  'use strict';

  var app = angular.module('radar.core');

  app.directive('rrSort', function() {
    return {
      restrict: 'A',
      scope: {
        by: '=',
        reverse: '=',
        key: '@'
      },
      templateUrl: 'app/core/sort.html',
      transclude: true,
      link: function(scope) {
        scope.sort = function() {
          if (scope.by === scope.key) {
            scope.reverse = !scope.reverse;
          } else {
            scope.by = scope.key;
            scope.reverse = false;
          }
        };
      }
    };
  });
})();

