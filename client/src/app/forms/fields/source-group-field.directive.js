(function() {
  'use strict';

  var app = angular.module('radar.forms.fields');

  app.directive('frmSourceGroupField', ['store', 'session', '_', 'sortGroups', function(store, session, _, sortGroups) {
    return {
      restrict: 'A',
      scope: {
        patient: '=',
        model: '=',
        required: '&'
      },
      templateUrl: 'app/forms/fields/source-group-field.html',
      link: function(scope) {
        var user = session.user;
        var isAdmin = user.isAdmin;

        var groupIds = [];

        if (!isAdmin) {
          var userGroups = user.groups;

          _.forEach(userGroups, function(userGroup) {
            if (userGroup.hasPermission('EDIT_PATIENT')) {
              groupIds.push(userGroup.group.id);
            }
          });
        }

        var patientGroups = scope.patient.groups;
        var sourceGroups = [];

        _.forEach(patientGroups, function(patientGroup) {
          if (patientGroup.group.type === 'HOSPITAL' && (isAdmin || groupIds.indexOf(patientGroup.group.id) >= 0)) {
            sourceGroups.push(patientGroup.group);
          }
        });

        sourceGroups = sortGroups(sourceGroups);

        if (!scope.model) {
          scope.model = sourceGroups[0];
        }

        scope.sourceGroups = sourceGroups;
      }
    };
  }]);
})();
