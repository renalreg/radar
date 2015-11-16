(function() {
  'use strict';

  var app = angular.module('radar.patients');

  function PatientDetailController(
    $scope,
    patient,
    session,
    hasDemographicsPermissionForPatient
  ) {
    $scope.patient = patient;
    $scope.demographicsPermission = hasDemographicsPermissionForPatient(session.user, patient);
  }

  PatientDetailController.$inject = [
    '$scope',
    'patient',
    'session',
    'hasDemographicsPermissionForPatient'
  ];

  app.controller('PatientDetailController', PatientDetailController);
})();
