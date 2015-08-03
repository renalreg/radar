(function() {
  'use strict';

  var app = angular.module('radar.patients');

  app.controller('PatientDetailController', function($scope, patient) {
    $scope.patient = patient;
  });
})();
