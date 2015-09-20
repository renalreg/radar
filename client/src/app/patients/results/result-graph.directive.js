(function() {
  'use strict';

  var app = angular.module('radar.patients.results');

  app.directive('resultGraph', function(Highcharts) {
    return {
      scope: {
        resultSpec: '=',
        resultGroups: '='
      },
      link: function(scope, element) {
        scope.$watch('resultSpec', load);
        scope.$watch('resultGroups', load);

        function load() {
          var resultSpec = scope.resultSpec;
          var resultGroups = scope.resultGroups;

          if (!resultSpec || !resultGroups) {
            return;
          }

          var data = [];

          _.forEach(resultGroups, function(x) {
            data.push({
              x: Date.parse(x.date),
              y: x.getValue(resultSpec.code),
              dataSource: x.dataSource.getName()
            });
          });

          data = _.sortBy(data, 'x');

          var options = {
            chart: {
              zoomType: 'x',
              renderTo: element.get(0)
            },
            title: {
              text: resultSpec.name
            },
            xAxis: {
              type: 'datetime'
            },
            yAxis: {
              title: {
                text: resultSpec.units
              }
            },
            series: [{
              name: resultSpec.shortName,
              data: data
            }],
            plotOptions: {
              line: {
                marker: {
                  enabled: true
                }
              }
            },
            tooltip: {
              pointFormat: '<span style="color:{point.color}">\u25CF</span> {series.name}: <b>{point.y}</b> ({point.dataSource})<br/>',
            }
          };

          new Highcharts.Chart(options);
        }
      }
    };
  });
})();
