(function() {
  'use strict';

  var app = angular.module('radar');

  var CHANGE_PASSWORD_STATE = 'changePassword';

  function run(
    $rootScope,
    radar,
    getValueAtPath,
    session,
    $state,
    notificationService,
    sessionTimeoutService
  ) {
    $rootScope.$watch(function() {
      return radar.ready;
    }, function(ready) {
      $rootScope.ready = ready;
    });

    sessionTimeoutService.init();

    function isPublicState(state) {
      return getValueAtPath(state, 'data.public');
    }

    // Users that haven't logged in can only view public pages
    $rootScope.$on('$stateChangeStart', function(event, toState) {
      if (!isPublicState(toState)) {
        radar.readyPromise.then(function() {
          if (!session.isAuthenticated) {
            event.preventDefault();
            $state.go('login');
          }
        });
      }
    });

    // Force the user to change their password
    $rootScope.$on('$stateChangeStart', function(event, toState) {
      if (!isPublicState(toState) && toState.name !== CHANGE_PASSWORD_STATE) {
        var user = session.user;

        if (user !== null && user.forcePasswordChange) {
          event.preventDefault();
          notificationService.info({
            title: 'Attention',
            message: 'Please update your password.'
          });
          $state.go(CHANGE_PASSWORD_STATE);
        }
      }
    });
  }

  run.$inject = [
    '$rootScope',
    'radar',
    'getValueAtPath',
    'session',
    '$state',
    'notificationService',
    'sessionTimeoutService'
  ];

  app.run(run);
})();
