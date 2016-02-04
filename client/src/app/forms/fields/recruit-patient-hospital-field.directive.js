(function() {
  'use strict';

  var app = angular.module('radar.forms.fields');

  function factory(_, session, hospitalStore, sortHospitals, hasPermissionForGroup) {
    return {
      restrict: 'A',
      scope: {
        model: '=',
        required: '&'
      },
      templateUrl: 'app/forms/fields/hospital-field.html',
      link: function(scope) {
        scope.$watch(function() {
          return session.user;
        }, function(user) {
          setHospitals([]);

          hospitalStore.findMany().then(function(hospitals) {
            hospitals = _.filter(hospitals, function(x) {
              return hasPermissionForGroup(user, x, 'RECRUIT_PATIENT', true);
            });

            setHospitals(hospitals);
          });
        });

        function setHospitals(hospitals) {
          scope.hospitals = sortHospitals(hospitals);
        }
      }
    };
  }

  factory.$inject = ['_', 'session', 'hospitalStore', 'sortHospitals', 'hasPermissionForGroup'];

  app.directive('frmRecruitPatientHospitalField', factory);
})();
