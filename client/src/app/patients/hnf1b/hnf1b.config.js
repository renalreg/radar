(function() {
  'use strict';

  var app = angular.module('radar.patients.hnf1b');

  app.config(['$stateProvider', function($stateProvider) {
    $stateProvider.state('patient.hnf1bClinicalPictures', {
      url: '/hnf1b-clinical-pictures',
      templateUrl: 'app/patients/hnf1b/clinical-pictures.html'
    });
  }]);
})();
