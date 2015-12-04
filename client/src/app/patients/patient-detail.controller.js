(function() {
  'use strict';

  var app = angular.module('radar.patients');

  function PatientDetailController(
    $scope,
    patient,
    session,
    hasGroupPermissionForPatient
  ) {
    $scope.patient = patient;
    $scope.showDemographics = hasGroupPermissionForPatient(session.user, patient, 'VIEW_DEMOGRAPHICS');
  }

  PatientDetailController.$inject = [
    '$scope',
    'patient',
    'session',
    'hasGroupPermissionForPatient'
  ];

  app.controller('PatientDetailController', PatientDetailController);
})();
