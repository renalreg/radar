(function() {
  'use strict';

  var app = angular.module('radar.permissions');

  app.factory('hasPermissionForUser', ['_', function(_) {
    return function hasPermissionForUser(user, otherUser, permission) {
      if (user === null) {
        return false;
      }

      if (user.isAdmin) {
        return true;
      }

      // Can view and edit yourself
      if (user.id == otherUser.id && (permission == 'VIEW_USER' || permission == 'EDIT_USER')) {
        return true;
      }

      var otherUserGroupIds = _.map(otherUser.groups, function(userGroup) {
        return userGroup.group.id;
      });

      var userGroups = user.groups;

      for (var i = 0; i < userGroups.length; i++) {
        var userGroup = userGroups[i];

        if (_.indexOf(otherUserGroupIds, userGroup.group.id) >= 0 && userGroup.hasPermission(permission)) {
          return true;
        }
      }

      return false;
    };
  }]);
})();
