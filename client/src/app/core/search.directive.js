(function() {
  'use strict';

  var app = angular.module('radar.core');

  app.directive('rrSearch', function() {
    return {
      restrict: 'A',
      templateUrl: 'app/core/search.html',
      scope: {
        search: '='
      },
      link: function(scope) {
        scope.clear = clear;

        function clear() {
          scope.search = '';
        }
      }
    };
  });
})();
