(function() {
  'use strict';

  var app = angular.module('radar.stats');

  app.directive('patientsByRecruitedGroupTable', ['adapter', '_', function(adapter, _) {
    return {
      scope: {
        group: '='
      },
      templateUrl: 'app/stats/patients-by-recruited-group-table.html',
      link: function(scope) {
        scope.loading = true;

        scope.$watch('group', function(group) {
          var params = {};

          console.log(group);

          if (group) {
            params.group = group.id;
          }

          scope.loading = true;

          adapter.get('/patients-by-recruited-group', params).then(function(response) {
            scope.loading = false;
            scope.counts = _.sortBy(response.data.counts, 'count').reverse();
          });
        });
      }
    };
  }]);
})();
