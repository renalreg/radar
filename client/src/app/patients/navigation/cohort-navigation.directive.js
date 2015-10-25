(function() {
  'use strict';

  var app = angular.module('radar.patients.navigation');

  app.directive('cohortNavigation', ['patientFeatures', '_', function(patientFeatures, _) {
    return {
      scope: {
        patient: '=',
        cohort: '='
      },
      templateUrl: 'app/patients/navigation/cohort-navigation.html',
      link: function(scope) {
        scope.items = [];

        var features = scope.cohort.features;

        _.forEach(features, function(x) {
          var item = patientFeatures[x];

          if (item !== undefined) {
            scope.items.push(item);
          }
        });
      }
    };
  }]);
})();
