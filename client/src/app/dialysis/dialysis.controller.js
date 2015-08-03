(function() {
  'use strict';

  var app = angular.module('radar.dialysis');

  app.controller('DialysisController', function($scope, patient) {
    $scope.patient = patient;
  });
})();
