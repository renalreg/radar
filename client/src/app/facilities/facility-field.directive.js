(function() {
  'use strict';

  var app = angular.module('radar.facilities');

  app.directive('facilityField', function(store, session, _) {
    return {
      restrict: 'A',
      scope: {
        patient: '=',
        model: '=',
        required: '='
      },
      templateUrl: 'app/facilities/facility-field.html',
      link: function(scope) {
        var user = session.user;
        var isAdmin = user.isAdmin;

        var unitIds = [];

        if (!isAdmin) {
          _.forEach(user.units, function(unit) {
            if (unit.hasEditPermission) {
              unitIds.push(unit.unit.id);
            }
          });
        }

        var facilities = [];

        var patientUnits = scope.patient.units;

        _.forEach(patientUnits, function(unit) {
          if (isAdmin || unitIds.indexOf(unit.unit.id) >= 0) {
            _.forEach(unit.unit.facilities, function(facilitiy) {
              if (facilitiy.isInternal) {
                facilities.push(facilitiy);
              }
            });
          }
        });

        facilities = _.sortBy(facilities, 'name');

        if (!scope.model) {
          scope.model = facilities[0];
        }

        scope.facilities = facilities;
      }
    };
  });
})();
