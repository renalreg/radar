(function() {
  'use strict';

  var app = angular.module('radar.patients.navigation');

  app.directive('patientNavigation', function(standardPatientFeatures, patientFeatures, _) {
    return {
      scope: {
        patient: '='
      },
      templateUrl: 'app/patients/navigation/patient-navigation.html',
      link: function(scope) {
        scope.items = [];

        _.forEach(standardPatientFeatures, function(x) {
          var item = patientFeatures[x];

          if (item !== undefined) {
            scope.items.push(item);
          }
        });
      }
    };
  });
})();
