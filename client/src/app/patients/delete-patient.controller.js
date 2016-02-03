(function() {
  'use strict';

  var app = angular.module('radar.patients');

  function DeletePatientController($scope, notificationService, $state) {
    $scope.remove = function(patient) {
      patient.remove()
        .then(function() {
          notificationService.success('Patient deleted.');
          $state.go('patients');
        })
        ['catch'](function() {
          notificationService.fail('Failed to delete patient.');
        });
    };
  }

  DeletePatientController.$inject = ['$scope', 'notificationService', '$state'];

  app.controller('DeletePatientController', DeletePatientController);
})();
