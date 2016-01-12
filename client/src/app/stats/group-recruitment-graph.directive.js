(function() {
  'use strict';

  var app = angular.module('radar.stats');

  app.directive('groupRecruitmentGraph', ['adapter', function(adapter) {
    return {
      scope: {
        group: '='
      },
      template: '<div loading="loading"><div recruitment-graph title="{{group.name}}" data="data" class="graph"></div></div>',
      link: function(scope) {

        scope.loading = true;

        scope.$watch('group', function(group) {
          if (!group) {
            return;
          }

          scope.loading = true;

          adapter.get('/recruitment-by-month', {group: group.id}).then(function(response) {
            scope.loading = false;
            scope.data = response.data.points;
          });
        });
      }
    };
  }]);
})();
