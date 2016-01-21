(function() {
  'use strict';

  var app = angular.module('radar.patients.diagnoses');

  app.directive('diagnosisSelector', [function() {
    return {
      templateUrl: 'app/patients/comorbidities/diagnosis-selector.html'
    };
  }]);
})();
