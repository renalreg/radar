(function() {
  'use strict';

  var app = angular.module('radar.patients.results');

  function factory(
    filterObservationsByNumeric,
    filterResultsByObservations,
    groupResultsByObservation
  ) {
    return function transformResultsForGraph(results, observations) {
      var filteredObservations = filterObservationsByNumeric(observations);
      var filteredResults = filterResultsByObservations(results, filteredObservations);
      var groups = groupResultsByObservation(filteredResults, filteredObservations);
      return groups;
    };
  }

  factory.$inject = [
    'filterObservationsByNumeric',
    'filterResultsByObservations',
    'groupResultsByObservation'
  ];

  app.factory('transformResultsForGraph', factory);
})();
