(function() {
  'use strict';

  var app = angular.module('radar.hospitals');

  app.controller('HospitalDetailController', ['$scope', 'hospital', function($scope, hospital) {
    $scope.hospital = hospital;
  }]);
})();
