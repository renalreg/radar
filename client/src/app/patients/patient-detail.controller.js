(function() {
  'use strict';

  var app = angular.module('radar.patients');

  function PatientDetailController(
    $scope,
    patient,
    session,
    hasDemographicsPermission
  ) {
    $scope.patient = patient;
    $scope.demographicsPermission = hasDemographicsPermission(patient, session.user);
  }

  PatientDetailController.$inject = [
    '$scope',
    'patient',
    'session',
    'hasDemographicsPermission'
  ];

  app.controller('PatientDetailController', PatientDetailController);
})();
