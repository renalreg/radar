(function() {
  'use strict';

  var app = angular.module('radar.sessions');

  function factory(
    notificationService,
    adapter,
    $timeout,
    authService,
    $state,
    session
  ) {
    // Session length in seconds
    var sessionTimeout = null;

    // Warn user session is about to end
    var warningTimeout = null;
    var warningNotification = null;

    // Logout user just before session expires
    var logoutTimeout = null;
    var logoutNotification = null;

    session.on('login', extend);
    session.on('refresh', extend);
    session.on('logout', cancel);

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
          authService.logout(true);
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
    'adapter',
    '$timeout',
    'authService',
    '$state',
    'session'
  ];

  app.factory('sessionTimeoutService', factory);
})();
