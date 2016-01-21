(function() {
  'use strict';

  var app = angular.module('radar.store');

  function unauthorizedResponseFactory($q, session, notificationService, $state) {
    return function(promise) {
      return promise['catch'](function(response) {
        // API endpoint requires login (token may have expired)
        if (response.status === 401) {
          session.logout();
          notificationService.info({message: 'You have been logged out.', timeout: 0});
          $state.go('login');
        }

        return $q.reject(response);
      });
    };
  }

  unauthorizedResponseFactory.$inject = [
    '$q', 'authService', 'notificationService', '$state'
  ];

  app.factory('unauthorizedResponse', unauthorizedResponseFactory);

  app.config(['adapterProvider', function(adapterProvider) {
    adapterProvider.afterResponse('unauthorizedResponse');
  }]);
})();
