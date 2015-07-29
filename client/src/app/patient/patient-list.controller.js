(function() {
  'use strict';

  var app = angular.module('radar.patient');

  app.controller('PatientListController', function($scope, PatientService) {
    $scope.patients = PatientService.getPatients().$object;
  });
})();
