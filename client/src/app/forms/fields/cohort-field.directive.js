(function() {
  'use strict';

  var app = angular.module('radar.forms.fields');

  app.directive('frmCohortField', function(_, session, store) {
    function sortCohorts(cohorts) {
      return _.sortBy(cohorts, function(x) {
        return x.name.toUpperCase();
      });
    }

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
  });
})();

