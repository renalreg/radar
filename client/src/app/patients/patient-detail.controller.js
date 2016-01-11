(function() {
  'use strict';

  var app = angular.module('radar.patients');

  function PatientDetailController(
    $scope,
    patient,
    session,
    hasPermissionForPatient
  ) {
    $scope.patient = patient;
    $scope.showDemographics = hasPermissionForPatient(session.user, patient, 'VIEW_DEMOGRAPHICS');
  }

  PatientDetailController.$inject = [
    '$scope',
    'patient',
    'session',
    'hasPermissionForPatient'
  ];

  app.controller('PatientDetailController', PatientDetailController);
})();
