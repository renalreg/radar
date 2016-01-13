(function() {
  'use strict';

  var app = angular.module('radar.patients.results');

  app.factory('groupResultsByObservation', ['_', function(_) {
    return function groupResultsByObservation(results, observations) {
      var groups = {};

      if (observations === undefined) {
        observations = [];
      } else {
        _.forEach(observations, function(observation) {
          var observationId = observation.id;

          if (groups[observationId] === undefined) {
            groups[observationId] = {
              observation: observation,
              results: [],
            };
          }
        });
      }

      // Group results by observation ID
      _.forEach(results, function(result) {
        var observation = result.observation;
        var observationId = observation.id;
        var group = groups[observationId];

        if (group === undefined) {
          groups[observationId] = {
            observation: observation,
            results: [],
          };
          group = groups[observationId];
          observations.push(observation);
        }

        group.results.push(result);
      });

      // Keep groups in the original order
      groups = _.map(observations, function(observation) {
        return groups[observation.id];
      });

      return groups;
    };
  }]);
})();
