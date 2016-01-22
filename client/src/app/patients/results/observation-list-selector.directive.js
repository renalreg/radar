(function() {
  'use strict';

  var app = angular.module('radar.patients.results');

  app.directive('observationListSelector', ['store', '_', function(store, _) {
    return {
      scope: {
        selectedObservations: '=observations'
      },
      templateUrl: 'app/patients/results/observation-list-selector.html',
      link: function(scope) {
        store.findMany('observations').then(function(observations) {
          scope.observations = observations;
        });

        scope.add = function(observation) {
          scope.remove(observation);
          scope.selectedObservations.push(observation);
        };

        scope.remove = function(observation) {
          _.pull(scope.selectedObservations, observation);
        };

        scope.up = function(observation) {
          var index = _.indexOf(scope.selectedObservations, observation);

          if (index > 0) {
            swap(scope.selectedObservations, index, index - 1);
          }
        };

        scope.down = function(observation) {
          var index = _.indexOf(scope.selectedObservations, observation);
          var lastIndex = scope.selectedObservations.length - 1;

          if (index < lastIndex) {
            swap(scope.selectedObservations, index, index + 1);
          }
        };

        function swap(array, x, y) {
          var temp = array[x];
          array[x] = array[y];
          array[y] = temp;
        }
      }
    };
  }]);
})();
