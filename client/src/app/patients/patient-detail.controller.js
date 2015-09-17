(function() {
  'use strict';

  var app = angular.module('radar.patients');

  app.controller('PatientDetailController', function($scope, patient, session, hasDemographicsPermission) {
    $scope.patient = patient;
    $scope.demographicsPermission = hasDemographicsPermission(patient, session.user);
  });
})();
