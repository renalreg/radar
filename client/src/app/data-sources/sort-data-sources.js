(function() {
  'use strict';

  var app = angular.module('radar.cohorts');

  app.factory('sortDataSources', ['_', function(_) {
    return function sortDataSources(dataSources) {
      return _.sortBy(dataSources, function(x) {
        return x.getName();
      });
    };
  }]);
})();
