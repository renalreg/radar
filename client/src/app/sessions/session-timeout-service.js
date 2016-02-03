(function() {
  'use strict';

  var app = angular.module('radar.sessions');

  function factory(
    notificationService,
    $rootScope,
    adapter,
    $timeout,
    authService,
    $state
  ) {
    // Session length in seconds
    var sessionTimeout = null;

    // Warn user session is about to end
    var warningTimeout = null;
    var warningNotification = null;

    // Logout user just before session expires
    var logoutTimeout = null;
    var logoutNotification = null;

    $rootScope.$on('sessions.login', extend);
    $rootScope.$on('sessions.refresh', extend);
    $rootScope.$on('sessions.logout', cancel);

    return {
      init: init
    };

    function init() {
      adapter.get('/environment').then(function(response) {
        sessionTimeout = response.data.sessionTimeout;
      });
    }

    function extend() {
      cancel();

      if (sessionTimeout !== null) {
        // Warn 3 minutes before session is due to end
        var warningDelay = (sessionTimeout - (3 * 60)) * 1000;

        warningTimeout = $timeout(function() {
          warningNotification = notificationService.warn({
            message: 'Session is about to expire.',
            timeout: 0
          });
        }, warningDelay);

        // Logout 1 minute before session is due to end
        var logoutDelay = (sessionTimeout - 60) * 1000;

        logoutTimeout = $timeout(function() {
          logoutNotification = notificationService.info({
            message: 'You were logged out due to inactivity.',
            timeout: 0
          });
          authService.logout();
          $state.go('login');
        }, logoutDelay);
      }
    }

    function cancel() {
      if (warningNotification !== null) {
        warningNotification.remove();
        warningNotification = null;
      }

      if (warningTimeout !== null) {
        $timeout.cancel(warningTimeout);
        warningTimeout = null;
      }

      if (logoutTimeout !== null) {
        $timeout.cancel(logoutTimeout);
        logoutTimeout = null;
      }

      if (logoutNotification !== null) {
        logoutNotification.remove();
        logoutNotification = null;
      }
    }
  }

  factory.$inject = [
    'notificationService',
    '$rootScope',
    'adapter',
    '$timeout',
    'authService',
    '$state'
  ];

  app.factory('sessionTimeoutService', factory);
})();
