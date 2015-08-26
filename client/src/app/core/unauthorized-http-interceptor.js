(function() {
  'use strict';

  var app = angular.module('radar.core');

  app.factory('unauthorizedHttpInterceptor', function($rootScope) {
    return {
      response: function(response) {
        if (response.status === 401) {
          $rootScope.$broadcast('unauthorized');
        }

        return response;
      }
    };
  });
})();


