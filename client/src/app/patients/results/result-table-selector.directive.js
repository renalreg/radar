(function() {
  'use strict';

  var app = angular.module('radar.patients.results');

  app.directive('resultTableSelector', ['store', '_', function(store, _) {
    return {
      scope: {
        selectedObservations: '=observations'
      },
      templateUrl: 'app/patients/results/result-table-selector.html',
      link: function(scope) {
        scope.add = add;
        scope.remove = remove;
        scope.change = change;

        store.findMany('observations').then(function(observations) {
          scope.observations = _.sortBy(observations, 'name');;
        });

        function change() {
          add(scope.selectedObservation);
          scope.selectedObservation = null;
        }

        function add(observation) {
          if (_.indexOf(scope.selectedObservation, observation) === -1) {
            scope.selectedObservations.push(observation);
          }
        }

        function remove(observation) {
          _.pull(scope.selectedObservations, observation);
        }
      }
    };
  }]);
})();
