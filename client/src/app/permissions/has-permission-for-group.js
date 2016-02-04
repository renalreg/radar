(function() {
  'use strict';

  var app = angular.module('radar.permissions');

  app.factory('hasPermissionForGroup', ['_', 'hasPermission', function(_, hasPermission) {
    return function hasPermissionForGroup(user, group, permission, explicit) {
      if (explicit === undefined) {
        explicit = false;
      }

      if (user === null) {
        return false;
      }

      if (user.isAdmin) {
        return true;
      }

      // Users get permissions on the RaDaR group through their other groups
      if (
        !explicit &&
        group.code === 'RADAR' &&
        group.type === 'OTHER' &&
        (
          permission === 'VIEW_PATIENT' ||
          permission === 'EDIT_PATIENT'
        )
      ) {
        return hasPermission(user, permission);
      }

      // Users get permissions on cohort groups through their hospital groups
      if (
        !explicit &&
        group.type === 'COHORT' &&
        (
          permission === 'VIEW_PATIENT' ||
          permission === 'EDIT_PATIENT' ||
          permission === 'RECRUIT_PATIENT' ||
          permission === 'EDIT_PATIENT_MEMBERSHIP'
        ) &&
        hasPermission(user, permission, 'HOSPITAL')
      ) {
        return true;
      }

      return _.some(user.groups, function(x) {
        return x.group.id === group.id && x.hasPermission(permission);
      });
    };
  }]);
})();
