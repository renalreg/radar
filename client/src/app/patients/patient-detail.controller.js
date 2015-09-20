(function() {
  'use strict';

  var app = angular.module('radar.patients');

  app.controller('PatientDetailController', ['$scope', 'patient', 'session', 'hasDemographicsPermission', function($scope, patient, session, hasDemographicsPermission) {
    $scope.patient = patient;
    $scope.demographicsPermission = hasDemographicsPermission(patient, session.user);
  }]);
})();
