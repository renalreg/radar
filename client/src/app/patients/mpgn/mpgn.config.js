(function() {
  'use strict';

  var app = angular.module('radar.patients.mpgn');

  app.config(['$stateProvider', function($stateProvider) {
    $stateProvider.state('patient.mpgnClinicalPictures', {
      url: '/mpgn-clinical-pictures',
      templateUrl: 'app/patients/mpgn/clinical-pictures.html'
    });
  }]);
})();
