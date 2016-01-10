(function() {
  'use strict';

  var app = angular.module('radar.patients.results');

  app.directive('resultGraphsComponent', ['store', function(store) {
    return {
      scope: {
        patient: '='
      },
      templateUrl: 'app/patients/results/result-graphs-component.html',
      link: function(scope) {
        scope.selectedObservation = null;
        scope.results = [];
        scope.loading = true;

        scope.$watch('selectedObservation', function(selectedObservation) {
          if (selectedObservation) {
            scope.loading = true;

            var params = {
              patient: scope.patient.id,
              observationId: selectedObservation.id
            };

            store.findMany('results', params).then(function(results) {
              scope.loading = false;
              scope.results = results;
            });
          }
        });
      }
    };
  }]);
})();
