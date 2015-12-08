(function() {
  'use strict';

  var app = angular.module('radar.stats');

  app.directive('cohortRecruitmentGraph', ['adapter', function(adapter) {
    return {
      scope: {
        cohort: '='
      },
      template: '<div loading="loading"><div recruitment-graph title="{{cohort.name}}" data="data" class="graph"></div></div>',
      link: function(scope) {
        scope.loading = true;

        scope.$watch('cohort', function(cohort) {
          if (!cohort) {
            return;
          }

          scope.loading = true;

          adapter.get('/cohort-recruitment-timeline', {cohort: cohort.id}).then(function(response) {
            scope.loading = false;
            scope.data = response.data.points;
          });
        });
      }
    };
  }]);
})();
