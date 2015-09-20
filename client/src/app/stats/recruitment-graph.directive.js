(function() {
  'use strict';

  var app = angular.module('radar.stats');

  app.directive('recruitmentGraph', ['Highcharts', '_', function(Highcharts, _) {
    return {
      scope: {
        title: '@',
        data: '='
      },
      link: function(scope, element) {
        scope.$watch('data', load);

        function load() {
          var data = scope.data;

          if (!data) {
            return;
          }

          var newData = [];
          var totalData = [];

          _.forEach(data, function(x) {
            var date = Date.parse(x.date);
            newData.push({x: date, y: x.new});
            totalData.push({x: date, y: x.total});
          });

          newData = _.sortBy(newData, 'x');
          totalData = _.sortBy(totalData, 'x');

          var options = {
            chart: {
              zoomType: 'x',
              renderTo: element.get(0)
            },
            title: {
              text: scope.title
            },
            xAxis: {
              type: 'datetime'
            },
            yAxis: {
              title: {
                text: 'Patients'
              },
              min: 0
            },
            series: [
              {name: 'New', data: newData},
              {name: 'Total', data: totalData}
            ],
            plotOptions: {
              line: {
                marker: {
                  enabled: true
                }
              }
            }
          };

          new Highcharts.Chart(options);
        }
      }
    };
  }]);
})();
