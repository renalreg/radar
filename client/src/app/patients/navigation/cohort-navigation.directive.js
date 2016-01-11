(function() {
  'use strict';

  var app = angular.module('radar.patients.navigation');

  app.directive('cohortNavigation', ['patientPages', '_', function(patientPages, _) {
    return {
      scope: {
        patient: '=',
        cohort: '='
      },
      templateUrl: 'app/patients/navigation/cohort-navigation.html',
      link: function(scope) {
        scope.items = [];

        var pages = scope.cohort.pages;

        _.forEach(pages, function(x) {
          var item = patientPages[x];

          if (item !== undefined) {
            scope.items.push(item);
          }
        });
      }
    };
  }]);
})();
