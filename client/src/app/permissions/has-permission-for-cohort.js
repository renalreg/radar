(function() {
  'use strict';

  var app = angular.module('radar.permissions');

  app.factory('hasPermissionForCohort', ['_', function(_) {
    return function hasPermissionForCohort(user, cohort, permission) {
      return (
        user !== null && (
          user.isAdmin ||
          _.any(user.cohorts, function(x) {
            return x.cohort.id === cohort.id && x.hasPermission(permission);
          })
        )
      );
    };
  }]);
})();
