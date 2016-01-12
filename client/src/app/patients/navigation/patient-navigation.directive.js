(function() {
  'use strict';

  var app = angular.module('radar.patients.navigation');

  app.directive('patientNavigation', ['_', 'sortCohorts', function(_, sortCohorts) {
    return {
      scope: {
        patient: '=',
      },
      templateUrl: 'app/patients/navigation/patient-navigation.html',
      link: function(scope) {
        scope.$watchCollection(function() {
          return scope.patient.getCurrentCohorts();
        }, function(cohorts) {
          scope.cohorts = sortCohorts(_.map(cohorts, function(x) {
            return x.group;
          }));
        });
      }
    };
  }]);
})();
