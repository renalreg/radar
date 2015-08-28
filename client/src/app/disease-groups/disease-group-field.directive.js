(function() {
  'use strict';

  var app = angular.module('radar.diseaseGroups');

  app.directive('diseaseGroupField', function(store, _) {
    return {
      restrict: 'A',
      scope: {
        patient: '=',
        model: '=',
        required: '='
      },
      templateUrl: 'app/disease-groups/disease-group-field.html',
      link: function(scope) {
        store.findMany('disease-groups').then(function(diseaseGroups) {
          scope.diseaseGroups = _.sortBy(diseaseGroups, function(x) {
            return x.name.toUpperCase();
          });

          if (!scope.model) {
            scope.model = scope.diseaseGroups[0];
          }
        });
      }
    };
  });
})();

