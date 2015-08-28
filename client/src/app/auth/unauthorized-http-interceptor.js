(function() {
  'use strict';

  var app = angular.module('radar.auth');

  app.factory('unauthorizedHttpInterceptor', function($rootScope, $q) {
    return {
      responseError: function(rejection) {
        if (rejection.status === 401) {
          $rootScope.$broadcast('unauthorized');
        }

        return $q.reject(rejection);
      }
    };
  });
})();
