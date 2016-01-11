(function() {
  'use strict';

  var app = angular.module('radar.stats');

  app.directive('recruitmentByGroupTable', ['adapter', '_', function(adapter, _) {
    return {
      scope: {
        group: '=',
        groupType: '@',
      },
      templateUrl: 'app/stats/recruitment-by-group-table.html',
      link: function(scope) {
        scope.loading = true;

        scope.$watch('group', function(group) {
          var params = {
            groupType: scope.groupType
          };

          if (group) {
            params.group = group.id;
          }

          scope.loading = true;

          adapter.get('/recruitment-by-group', params).then(function(response) {
            scope.loading = false;
            scope.counts = _.sortByOrder(response.data.counts, ['patientCount'], ['desc']);
          });
        });
      }
    };
  }]);
})();
