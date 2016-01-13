(function() {
  'use strict';

  var app = angular.module('radar.patients.results');

  app.factory('filterResultsByObservations', ['_', function(_) {
      return function filterResultsByObservations(results, observations) {
        var observationIds = _.map(observations, function(x) {
          return x.id;
        });

        results = _.filter(results, function(result) {
          var observationId = result.observation.id;
          return _.indexOf(observationIds, observationId) >= 0;
        });

        return results;
      };
  }]);
})();
