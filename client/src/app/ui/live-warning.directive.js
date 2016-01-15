(function() {
  'use strict';

  var app = angular.module('radar.ui');

  app.directive('liveWarning', ['adapter', function(adapter) {
    return {
      restrict: 'A',
      scope: true,
      templateUrl: 'app/ui/live-warning.html',
      link: function(scope) {
        scope.live = true;

        adapter.get('/environment').then(function(response) {
          scope.live = response.data.live;
        });
      }
    };
  }]);
})();
