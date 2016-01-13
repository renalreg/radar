(function() {
  'use strict';

  var app = angular.module('radar.patients.results');

  app.directive('resultGraphSelector', ['store', '_', function(store, _) {
    return {
      scope: {
        selectedObservation: '=observation'
      },
      templateUrl: 'app/patients/results/result-graph-selector.html',
      link: function(scope) {
        store.findMany('observations', {types: 'INTEGER,REAL'}).then(function(observations) {
          scope.observations = _.sortBy(observations, 'name');
        });
      }
    };
  }]);
})();
