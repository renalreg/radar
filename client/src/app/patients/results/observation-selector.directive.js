(function() {
  'use strict';

  var app = angular.module('radar.patients.results');

  app.directive('observationSelector', ['store', '_', function(store, _) {
    return {
      require: 'ngModel',
      templateUrl: 'app/patients/results/observation-selector.html',
      link: function(scope, element, attrs, ngModel) {
        scope.selectedObservation = null;

        store.findMany('observations').then(function(observations) {
          scope.observations = observations;
        });

        ngModel.$render = function() {
          scope.selectedObservation = ngModel.$viewValue;
        };

        scope.use = function(observation) {
          scope.selectedObservation = observation;
          ngModel.$setViewValue(observation);
        };
      }
    };
  }]);
})();
