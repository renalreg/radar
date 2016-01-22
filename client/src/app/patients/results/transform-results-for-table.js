(function() {
  'use strict';

  var app = angular.module('radar.patients.results');

  function factory(
    filterResultsByObservations,
    groupResults
  ) {
    return function transformResultsForTable(results, observations) {
      var filteredResults = filterResultsByObservations(results, observations);
      var groups = groupResults(filteredResults);
      return groups;
    };
  }

  factory.$inject = [
    'filterResultsByObservations',
    'groupResults'
  ];

  app.factory('transformResultsForTable', factory);
})();
