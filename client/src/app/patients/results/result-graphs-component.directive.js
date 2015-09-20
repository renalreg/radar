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
        scope.resultSpec = null;
        scope.resultGroups = [];
        scope.loading = true;

        scope.$watch('resultSpec', function(resultSpec) {
          if (resultSpec) {
            scope.loading = true;

            store.findMany('result-groups', {patient: scope.patient.id, resultCodes: resultSpec.code}).then(function(resultGroups) {
              scope.loading = false;
              scope.resultGroups = resultGroups;
            });
          }
        });
      }
    };
  }]);
})();
