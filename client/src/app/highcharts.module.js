/* globals Highcharts */

(function() {
  'use strict';

  var app = angular.module('highcharts', []);

  app.factory('Highcharts', function() {
    return Highcharts;
  });
})();
