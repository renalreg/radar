(function() {
  'use strict';

  var app = angular.module('radar.store');

  function unauthorizedResponseFactory($q, session, notificationService, $state) {
    var notification = null;

    // Hide logout notification on login
    session.on('login', function() {
      if (notification !== null) {
        notification.remove();
        notification = null;
      }
    });

    return function(promise) {
      return promise['catch'](function(response) {
        // API endpoint requires login (token may have expired)
        if (response.status === 401) {
          session.logout(true);

          if (notification === null) {
            notification = notificationService.info({message: 'You have been logged out.', timeout: 0});
          }

          $state.go('login');
        }

        return $q.reject(response);
      });
    };
  }

  unauthorizedResponseFactory.$inject = [
    '$q', 'session', 'notificationService', '$state'
  ];

  app.factory('unauthorizedResponse', unauthorizedResponseFactory);

  app.config(['adapterProvider', function(adapterProvider) {
    adapterProvider.afterResponse('unauthorizedResponse');
  }]);
})();
