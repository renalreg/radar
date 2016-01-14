(function() {
  'use strict';

  var app = angular.module('radar.patients.results');

  app.factory('groupResults', ['_', function(_) {
    function getKey(result) {
      return result.sourceGroup.id + '.' + result.sourceType + '.' + result.date;
    }

    return function groupResults(results) {
      var groups = [];
      var currentKey = null;
      var currentGroup = null;

      // Sort the results so they group properly
      results = _.sortBy(results, getKey);

      _.forEach(results, function(result) {
        var observationId = result.observation.id;

        var key = getKey(result);

        if (
          key !== currentKey ||
          currentGroup === null ||
          currentGroup.results[observationId] !== undefined
        ) {
          currentKey = key;
          currentGroup = {
            date: result.date,
            source: result.getSource(),
            results: {}
          };
          groups.push(currentGroup);
        }

        currentGroup.results[observationId] = result;
      });

      return groups;
    };
  }]);
})();
