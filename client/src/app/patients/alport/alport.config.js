(function() {
  'use strict';

  var app = angular.module('radar.patients.alport');

  app.config(['$stateProvider', function($stateProvider) {
    $stateProvider.state('patient.alportClinicalPictures', {
      url: '/alport-clinical-pictures',
      templateUrl: 'app/patients/alport/clinical-pictures.html'
    });
  }]);
})();
