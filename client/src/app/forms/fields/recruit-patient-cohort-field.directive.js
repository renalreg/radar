(function() {
  'use strict';

  var app = angular.module('radar.forms.fields');

  function factory(_, sortCohorts, cohortStore, session, hasPermissionForGroup) {
    return {
      restrict: 'A',
      scope: {
        model: '=',
        required: '&'
      },
      templateUrl: 'app/forms/fields/cohort-field.html',
      link: function(scope) {
        scope.$watch(function() {
          return session.user;
        }, function(user) {
          setCohorts([]);

          cohortStore.findMany({isRecruitmentGroup: true}).then(function(cohorts) {
            cohorts = _.filter(cohorts, function(x) {
              return hasPermissionForGroup(user, x, 'RECRUIT_PATIENT');
            });

            setCohorts(cohorts);
          });
        });

        function setCohorts(cohorts) {
          scope.cohorts = sortCohorts(cohorts);
        }
      }
    };
  }

  factory.$inject = ['_', 'sortCohorts', 'cohortStore', 'session', 'hasPermissionForGroup'];

  app.directive('frmRecruitPatientCohortField', factory);
})();
