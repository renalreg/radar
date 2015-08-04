(function() {
  'use strict';

  var app = angular.module('radar.core');

  app.factory('CurrentUserService', function() {
    return {
      getUser: getUser
    };

    function getUser() {
      return {
        id: 1
      };
    }
  });
})();
