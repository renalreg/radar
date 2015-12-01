(function() {
  'use strict';

  var app = angular.module('radar.permissions');

  app.factory('hasRecruitPatientPermission', ['_', function(_) {
    return function hasRecruitPatientPermission(user) {
      return user !== null && (user.isAdmin || _.any(user.organisations, function(x) {
        return x.hasRecruitPatientPermission;
      }));
    };
  }]);
})();
