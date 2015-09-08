(function() {
  'use strict';

  var app = angular.module('radar.patients.navigation');

  app.directive('radarNavigation', function(radarPatientFeatures, patientFeatures, _) {
    return {
      scope: {
        patient: '='
      },
      templateUrl: 'app/patients/navigation/radar-navigation.html',
      link: function(scope) {
        scope.links = [];

        _.forEach(radarPatientFeatures, function(x) {
          var link = patientFeatures[x];

          if (link !== undefined) {
            scope.links.push(link);
          }
        });
      }
    };
  });
})();


