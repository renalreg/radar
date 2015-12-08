(function() {
  'use strict';

  var app = angular.module('radar.stats');

  app.directive('recruitmentByOrganisationTable', ['adapter', '_', function(adapter, _) {
    return {
      scope: {
        cohort: '='
      },
      templateUrl: 'app/stats/recruitment-by-organisation-table.html',
      link: function(scope) {
        scope.loading = true;

        scope.$watch('cohort', function(cohort) {
          var params = {};

          if (cohort) {
            params.cohort = cohort.id;
          }

          scope.loading = true;

          adapter.get('/recruitment-by-organisation', params).then(function(response) {
            scope.loading = false;
            scope.counts = _.sortByOrder(response.data.counts, ['patientCount'], ['desc']);
          });
        });
      }
    };
  }]);
})();
