(function() {
  'use strict';

  var app = angular.module('radar.patients');

  function RecruitPatientController(
    $scope,
    adapter,
    $state
  ) {
    $scope.loading = false;

    $scope.searchParams = {};
    $scope.searchErrors = {};

    $scope.patient = {};

    $scope.search = function() {
      $scope.loading = true;

      adapter.post('/recruit-patient-search', {}, $scope.searchParams)
        .then(function(response) {
          var results = response.data.results;

          $scope.results = results;
          $scope.searchErrors = {};

          if (results) {
            $state.go('recruitPatient.results');
          } else {
            $scope.patient = {
              firstName: $scope.searchParams.firstName,
              lastName: $scope.searchParams.lastName,
              dateOfBirth: $scope.searchParams.dateOfBirth
            };

            $state.go('recruitPatient.consent');
          }
        })
        ['catch'](function(response) {
          if (response.status === 422) {
            $scope.searchErrors = response.data.errors || {};
          }
        })
        ['finally'](function() {
          $scope.loading = false;
        });
    };

    $scope.patientFound = function(result) {
      $scope.patient = {
        mpiid: result.mpiid,
        radarId: result.radarId,
        firstName: result.firstName,
        lastName: result.lastName,
        dateOfBirth: result.dateOfBirth,
        nhsNo: result.nhsNo,
        chiNo: result.chiNo
      };

      $state.go('recruitPatient.consent');
    };

    $scope.patientNotFound = function() {
      $scope.patient = {
        firstName: $scope.searchParams.firstName,
        lastName: $scope.searchParams.lastName,
        dateOfBirth: $scope.searchParams.dateOfBirth,
        nhsNo: $scope.searchParams.nhsNo,
        chiNo: $scope.searchParams.chiNo
      };

      $state.go('recruitPatient.consent');
    };

    $scope.recruit = function() {
      $scope.loading = true;

      adapter.post('/recruit-patient', {}, $scope.patient)
        .then(function(response) {
          var patientId = response.data.id;
          $state.go('patient.demographics', {patientId: patientId});
        })
        ['catch'](function(response) {
          if (response.status === 422) {
            $scope.recruitErrors = response.data.errors || {};
          }
        })
        ['finally'](function() {
          $scope.loading = false;
        });
    };

    $scope.backToSearch = function() {
      $state.go('recruitPatient.search');
    };

    $scope.backToResults = function() {
      $state.go('recruitPatient.results');
    };
  }

  RecruitPatientController.$inject = [
    '$scope',
    'adapter',
    '$state'
  ];

  app.controller('RecruitPatientController', RecruitPatientController);
})();
