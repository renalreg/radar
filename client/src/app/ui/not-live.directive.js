(function() {
  'use strict';

  var app = angular.module('radar.ui');

  app.directive('notLive', ['adapter', function(adapter) {
    return {
      restrict: 'A',
      scope: true,
      templateUrl: 'app/ui/not-live.html',
      link: function(scope) {
        scope.live = true;

        adapter.get('/environment').then(function(environment) {
          scope.live = environment.live;
        });
      }
    };
  }]);
})();
