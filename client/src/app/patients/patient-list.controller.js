(function() {
  'use strict';

  var app = angular.module('radar.patients');

  app.controller('PatientListController', function($scope, patients) {
    $scope.patients = patients;
  });
})();
