(function() {
  'use strict';

  var app = angular.module('radar.patients.results');

  app.directive('resultListSelector', function (store) {
    var INITIAL_RESULT_CODES = ['CREATININE'];

    return {
      scope: {
        selectedResultSpecs: '=resultSpecs'
      },
      templateUrl: 'app/patients/results/result-list-selector.html',
      link: function(scope) {
        scope.add = add;
        scope.remove = remove;
        scope.change = change;

        store.findMany('result-specs').then(function(resultSpecs) {
          scope.resultSpecs = resultSpecs;

          var resultCodeToSpec = {};

          _.forEach(resultSpecs, function(x) {
            resultCodeToSpec[x.code] = x;
          });

          _.forEach(INITIAL_RESULT_CODES, function(x) {
            var resultSpec = resultCodeToSpec[x];

            if (resultSpec !== undefined) {
              add(resultSpec);
            }
          });
        });

        function change() {
          add(scope.selectedResultSpec);
          scope.selectedResultSpec = null;
        }

        function add(resultSpec) {
          var duplicate = _.any(scope.selectedResultSpecs, function (x) {
            return x.code == resultSpec.code;
          });

          if (!duplicate) {
            scope.selectedResultSpecs.push(resultSpec);
          }
        }

        function remove(resultSpec) {
          _.pull(scope.selectedResultSpecs, resultSpec);
        }
      }
    };
  });
})();
