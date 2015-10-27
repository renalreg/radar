(function() {
  'use strict';

  var app = angular.module('radar.ui');

  app.directive('notLiveWarning', ['adapter', function(adapter) {
    return {
      restrict: 'A',
      scope: true,
      templateUrl: 'app/ui/not-live-warning.html',
      link: function(scope) {
        scope.live = true;

        adapter.get('/environment').then(function(environment) {
          scope.live = environment.live;
        });
      }
    };
  }]);
})();
