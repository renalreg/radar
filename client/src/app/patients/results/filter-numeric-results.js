(function() {
  'use strict';

  var app = angular.module('radar.patients.results');

  app.factory('filterNumericResults', ['_', function(_) {
      return function filterNumericResults(results) {
        return _.filter(results, function(result) {
          var valueType = result.observation.valueType.id;
          return valueType === 'INTEGER' || valueType === 'REAL';
        });
      };
  }]);
})();
