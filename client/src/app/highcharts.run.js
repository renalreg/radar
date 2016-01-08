(function() {
  'use strict';

  var app = angular.module('radar');

  app.run(['Highcharts', function(Highcharts) {
    Highcharts.setOptions({
      global: {
        // Don't convert datetimes to UTC (causes BST issues)
        useUTC: false
      }
    })
  }]);
})();
