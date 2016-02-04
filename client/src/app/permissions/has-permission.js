(function() {
  'use strict';

  var app = angular.module('radar.permissions');

  app.factory('hasPermission', ['_', function(_) {
    return function hasPermission(user, permission, groupType) {
      if (user === null) {
        return false;
      }

      if (user.isAdmin) {
        return true;
      }

      var groups = user.groups;

      if (groupType !== undefined) {
        groups = _.filter(groups, function(x) {
          return x.group.type === groupType;
        });
      }

      return _.some(groups, function(x) {
        return x.hasPermission(permission);
      });
    };
  }]);
})();
