(function() {
  'use strict';

  var app = angular.module('radar.renalImaging');

  app.controller('RenalImagingController', function($scope, patient) {
    $scope.patient = patient;
  });
})();

