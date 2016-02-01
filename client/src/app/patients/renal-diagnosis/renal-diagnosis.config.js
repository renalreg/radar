(function() {
  'use strict';

  var app = angular.module('radar.patients.renalDiagnosis');

  app.config(['$stateProvider', function($stateProvider) {
    $stateProvider.state('patient.renalDiagnosis', {
      url: '/renal-diagnosis',
      templateUrl: 'app/patients/renal-diagnosis/renal-diagnosis.html'
    });
  }]);
})();
