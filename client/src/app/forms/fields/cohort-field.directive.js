(function() {
  'use strict';

  var app = angular.module('radar.forms.fields');

  app.directive('frmCohortField', ['sortCohorts', 'session', 'store', function(sortCohorts, session, store) {
    return {
      restrict: 'A',
      scope: {
        model: '=',
        required: '&'
      },
      templateUrl: 'app/forms/fields/cohort-field.html',
      link: function(scope) {
        store.findMany('cohorts').then(function(cohorts) {
          scope.cohorts = sortCohorts(cohorts);
        });
      }
    };
  }]);
})();

