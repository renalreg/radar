(function() {
  'use strict';

  var app = angular.module('radar.store');

  function forbiddenResponseFactory($q, notificationService) {
    return function(promise) {
      return promise['catch'](function(response) {
        if (response.status === 403) {
          notificationService.fatal({
            title: 'Forbidden',
            message: 'You don\'t have permission to perform that action.'
          });
        }

        return $q.reject(response);
      });
    };
  }

  forbiddenResponseFactory.$inject = [
    '$q', 'notificationService'
  ];

  app.factory('forbiddenResponse', forbiddenResponseFactory);

  app.config(['adapterProvider', function(adapterProvider) {
    adapterProvider.afterResponse('forbiddenResponse');
  }]);
})();
