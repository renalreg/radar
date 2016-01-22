(function() {
  'use strict';

  var app = angular.module('radar.patients.diagnoses');

  app.factory('PatientDiagnosisPermission', ['PatientSourceObjectPermission', function(PatientSourceObjectPermission) {
    return PatientSourceObjectPermission;
  }]);
})();
