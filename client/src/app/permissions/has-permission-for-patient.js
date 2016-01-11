(function() {
  'use strict';

  var app = angular.module('radar.permissions');

  app.factory('hasPermissionForPatient', ['_', function(_) {
    return function hasPermissionForPatient(user, patient, permission) {
      if (user === null) {
        return false;
      }

      if (user.isAdmin) {
        return true;
      }

      var patientGroupIds = _.map(patient.groups, function(patientGroup) {
        return patientGroup.group.id;
      });

      var userGroups = user.groups;

      for (var i = 0; i < userGroups.length; i++) {
        var userGroup = userGroups[i];

        if (_.indexOf(patientGroupIds, userGroup.group.id) >= 0 && userGroup.hasPermission(permission)) {
          return true;
        }
      }

      return false;
    };
  }]);
})();
