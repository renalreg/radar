(function() {
  'use strict';

  var app = angular.module('radar.stats');

  app.directive('organisationRecruitmentGraph', ['adapter', function(adapter) {
    return {
      scope: {
        organisation: '='
      },
      template: '<div loading="loading"><div recruitment-graph title="{{organisation.name}}" data="data" class="graph"></div></div>',
      link: function(scope) {
        scope.loading = true;

        scope.$watch('organisation', function(organisation) {
          if (!organisation) {
            return;
          }

          scope.loading = true;

          adapter.get('/organisation-recruitment-timeline', {organisation: organisation.id}).then(function(response) {
            scope.loading = false;
            scope.data = response.data.points;
          });
        });
      }
    };
  }]);
})();
