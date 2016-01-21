(function() {
  'use strict';

  var app = angular.module('radar.patients.diagnoses');

  app.directive('diagnosisSelector', ['store', function(store) {
    return {
      require: 'ngModel',
      templateUrl: 'app/patients/diagnoses/diagnosis-selector.html',
      link: function(scope, element, attrs, ngModel) {
        scope.selectedDiagnosis = null;

        store.findMany('diagnoses').then(function(diagnoses) {
          scope.diagnoses = diagnoses;
        });

        ngModel.$render = function() {
          scope.selectedDiagnosis = ngModel.$viewValue;
        };

        scope.use = function(diagnosis) {
          update(diagnosis);
        };

        scope.drop = function() {
          update(null);
        };

        function update(diagnosis) {
          scope.selectedDiagnosis = diagnosis;
          ngModel.$setViewValue(diagnosis);
        }
      }
    };
  }]);
})();
