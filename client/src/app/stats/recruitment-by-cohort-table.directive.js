(function() {
  'use strict';

  var app = angular.module('radar.stats');

  app.directive('recruitmentByCohortTable', ['adapter', '_', function(adapter, _) {
    return {
      scope: {
        organisation: '='
      },
      templateUrl: 'app/stats/recruitment-by-cohort-table.html',
      link: function(scope) {
        scope.loading = true;

        scope.$watch('organisation', function(organisation) {
          var params = {};

          if (organisation) {
            params.organisation = organisation.id;
          }

          scope.loading = true;

          adapter.get('/recruitment-by-cohort', params).then(function(response) {
            scope.loading = false;
            scope.counts = _.sortByOrder(response.data.counts, ['patientCount'], ['desc']);
          });
        });
      }
    };
  }]);
})();
