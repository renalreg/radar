(function() {
  'use strict';

  var app = angular.module('radar.patients.medications');

  app.directive('drugSelector', ['store', function(store) {
    return {
      require: 'ngModel',
      templateUrl: 'app/patients/medications/drug-selector.html',
      link: function(scope, element, attrs, ngModel) {
        scope.selectedDrug = null;

        store.findMany('drugs').then(function(drugs) {
          scope.drugs = drugs;
        });

        ngModel.$render = function() {
          scope.selectedDrug = ngModel.$viewValue;
        };

        scope.use = function(drug) {
          update(drug);
        };

        scope.drop = function() {
          update(null);
        };

        function update(drug) {
          scope.selectedDrug = drug;
          ngModel.$setViewValue(drug);
        }
      }
    };
  }]);
})();
