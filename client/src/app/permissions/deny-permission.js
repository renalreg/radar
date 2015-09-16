(function() {
  'use strict';

  var app = angular.module('radar.permissions');

  app.factory('DenyPermission', function() {
    function DenyPermission() {
    }

    DenyPermission.prototype.hasPermission = function() {
      return false;
    };

    DenyPermission.prototype.hasObjectPermission = function() {
      return false;
    };

    return DenyPermission;
  });
})();
