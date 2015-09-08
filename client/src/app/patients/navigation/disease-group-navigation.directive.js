(function() {
  'use strict';

  var app = angular.module('radar.patients.navigation');

  app.directive('diseaseGroupNavigation', function(patientFeatures, _) {
    return {
      scope: {
        patient: '=',
        diseaseGroup: '='
      },
      templateUrl: 'app/patients/navigation/disease-group-navigation.html',
      link: function(scope) {
        scope.links = [];

        var features = scope.diseaseGroup.features;
        _.sortBy(features, 'weight');

        _.forEach(features, function(x) {
          var link = patientFeatures[x.name];

          if (link !== undefined) {
            scope.links.push(link);
          }
        });
      }
    };
  });
})();

