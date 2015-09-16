(function() {
  'use strict';

  var app = angular.module('radar.permissions');

  app.factory('GrantPermission', function() {
    function GrantPermission() {
    }

    GrantPermission.prototype.hasPermission = function() {
      return true;
    };

    GrantPermission.prototype.hasObjectPermission = function() {
      return true;
    };

    return GrantPermission;
  });
})();
