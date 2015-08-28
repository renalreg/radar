(function() {
  'use strict';

  var app = angular.module('radar.ui');

  app.directive('loading', function() {
    return {
      restrict: 'A',
      scope: {
        loading: '='
      },
      transclude: true,
      templateUrl: 'app/ui/loading.html',
      link: function(scope) {
        scope.isLoading = function() {
          return scope.loading;
        };
      }
    };
  });
})();


