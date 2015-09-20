(function() {
  'use strict';

  var app = angular.module('radar.patients.results');

  app.directive('resultGraphSelector', ['store', '_', function(store, _) {
    return {
      scope: {
        resultSpec: '='
      },
      templateUrl: 'app/patients/results/result-graph-selector.html',
      link: function(scope) {
        store.findMany('result-specs').then(function(resultSpecs) {
          scope.resultSpecs = resultSpecs = _.sortBy(_.filter(resultSpecs, function(x) {
            return x.type === 'INTEGER' || x.type === 'FLOAT';
          }), 'name');

          if (resultSpecs) {
            scope.resultSpec = _.find(resultSpecs, function(x) {
              return x.code === 'CREATININE';
            });
          }
        });
      }
    };
  }]);
})();
