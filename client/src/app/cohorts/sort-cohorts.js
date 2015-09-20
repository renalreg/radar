(function() {
  'use strict';

  var app = angular.module('radar.cohorts');

  app.factory('sortCohorts', ['_', function(_) {
    return function sortCohorts(cohorts) {
      return _.sortBy(cohorts, function(x) {
        return x.name.toUpperCase();
      });
    };
  }]);
})();
