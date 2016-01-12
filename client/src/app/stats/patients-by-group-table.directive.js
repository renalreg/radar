(function() {
  'use strict';

  var app = angular.module('radar.stats');

  app.directive('patientsByGroupTable', ['adapter', '_', function(adapter, _) {
    return {
      scope: {
        group: '=',
        groupType: '@',
      },
      templateUrl: 'app/stats/patients-by-group-table.html',
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

          adapter.get('/patients-by-group', params).then(function(response) {
            scope.loading = false;
            scope.counts = _.sortByOrder(response.data.counts, ['patientCount'], ['desc']);
          });
        });
      }
    };
  }]);
})();
