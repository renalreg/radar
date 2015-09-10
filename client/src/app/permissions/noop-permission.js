(function() {
  'use strict';

  var app = angular.module('radar.permissions');

  app.factory('noopPermission', function() {
    return {
      hasPermission: function() {
        return true;
      },
      hasObjectPermission: function() {
        return true;
      }
    };
  });
})();
