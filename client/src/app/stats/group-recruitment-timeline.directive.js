(function() {
  'use strict';

  var app = angular.module('radar.stats');

  app.directive('groupRecruitmentTimeline', ['adapter', function(adapter) {
    return {
      scope: {
        group: '='
      },
      template: '<div loading="loading"><div recruitment-timeline title="{{group.name}}" data="data" class="graph"></div></div>',
      link: function(scope) {

        scope.loading = true;

        scope.$watch('group', function(group) {
          if (!group) {
            return;
          }

          scope.loading = true;

          adapter.get('/recruitment-timeline', {group: group.id}).then(function(response) {
            scope.loading = false;
            scope.data = response.data.points;
          });
        });
      }
    };
  }]);
})();
