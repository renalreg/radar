(function() {
  'use strict';

  var app = angular.module('radar.patient');

  app.controller('PatientDetailController', function($scope, patient) {
    $scope.patient = patient;
  });
})();
