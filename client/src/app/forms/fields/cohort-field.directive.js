(function() {
  'use strict';

  var app = angular.module('radar.forms.fields');

  app.directive('frmCohortField', ['sortCohorts', 'session', 'cohortStore', function(sortCohorts, session, cohortStore) {
    return {
      restrict: 'A',
      scope: {
        model: '=',
        required: '&'
      },
      templateUrl: 'app/forms/fields/cohort-field.html',
      link: function(scope) {
        cohortStore.findMany().then(function(cohorts) {
          scope.cohorts = sortCohorts(cohorts);
        });
      }
    };
  }]);
})();
