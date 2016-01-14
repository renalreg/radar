(function() {
  'use strict';

  var app = angular.module('radar.patients.comorbidities');

  app.directive('disorderSelector', [function() {
    return {
      templateUrl: 'app/patients/comorbidities/disorder-selector.html'
    };
  }]);
})();
