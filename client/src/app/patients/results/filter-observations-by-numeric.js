(function() {
  'use strict';

  var app = angular.module('radar.patients.results');

  app.factory('filterObservationsByNumeric', ['_', function(_) {
      return function filterObservationsByNumeric(observations) {
        return _.filter(observations, function(observation) {
          var valueType = observation.valueType.id;
          return valueType === 'INTEGER' || valueType === 'REAL';
        });
      };
  }]);
})();
