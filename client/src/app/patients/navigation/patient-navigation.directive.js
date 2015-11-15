(function() {
  'use strict';

  var app = angular.module('radar.patients.navigation');

  app.directive('patientNavigation', ['_', function(_) {
    return {
      scope: {
        patient: '=',
      },
      templateUrl: 'app/patients/navigation/patient-navigation.html',
      link: function(scope) {
        scope.$watchCollection('patient.cohorts', function(cohorts) {
          // Sort by cohort name with RaDaR on top
          scope.cohorts = _.sortByAll(cohorts, [function(cohort) {
            return cohort.cohort.code === 'RADAR' ? 0 : 1;
          }, 'cohort.name']);
        });
      }
    };
  }]);
})();
