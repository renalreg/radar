(function() {
  'use strict';

  var app = angular.module('radar.patients.navigation');

  app.directive('cohortNavigation', function(patientFeatures, _) {
    return {
      scope: {
        patient: '=',
        cohort: '='
      },
      templateUrl: 'app/patients/navigation/cohort-navigation.html',
      link: function(scope) {
        scope.items = [];

        var features = scope.cohort.features;
        _.sortBy(features, 'weight');

        _.forEach(features, function(x) {
          var item = patientFeatures[x.name];

          if (item !== undefined) {
            scope.items.push(item);
          }
        });
      }
    };
  });
})();

