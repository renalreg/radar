(function() {
  'use strict';

  var app = angular.module('radar');

  app.run(['$rootScope', 'radar', 'getValueAtPath', 'session', '$state', function($rootScope, radar, getValueAtPath, session, $state) {
    $rootScope.$watch(function() {
      return radar.ready;
    }, function(ready) {
      $rootScope.ready = ready;
    });

    $rootScope.$on('$stateChangeStart', function(event, toState) {
      var publicState = getValueAtPath(toState, 'data.public');

      if (!publicState) {
        radar.readyPromise.then(function() {
          if (session.getUserId() === null) {
            event.preventDefault();
            $state.go('login');
          }
        });
      }
    });
  }]);
})();
