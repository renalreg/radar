(function() {
  'use strict';

  var app = angular.module('radar');

  app.controller('PatientListController', function($scope, PatientService) {
    $scope.patients = PatientService.getPatients().$object;
  });
})();
