(function() {
  'use strict';

  var app = angular.module('radar.patients.ins');

  app.config(['$stateProvider', function($stateProvider) {
    $stateProvider.state('patient.insClinicalPictures', {
      url: '/ins-clinical-pictures',
      templateUrl: 'app/patients/ins/clinical-pictures.html'
    });
  }]);

  app.config(['$stateProvider', function($stateProvider) {
    $stateProvider.state('patient.insRelapses', {
      url: '/ins-relapses',
      templateUrl: 'app/patients/ins/relapses.html'
    });
  }]);
})();
