(function() {
  'use strict';

  var app = angular.module('radar.recruitPatient');

  function RecruitPatientController(
    $scope,
    adapter,
    $state,
    $q,
    store
  ) {
    $scope.loading = true;

    $q.all([
      store.findMany('genders').then(function(genders) {
        $scope.genders = genders;
      }),
      store.findMany('ethnicity-codes').then(function(ethnicityCodes) {
        $scope.ethnicityCodes = ethnicityCodes;
      })
    ]).then(function() {
      $scope.loading = false;
    });

    $scope.searchParams = {};
    $scope.searchErrors = {};

    $scope.patient = {};
    $scope.patientErrors = {};

    $scope.search = search;
    $scope.patientFound = patientFound;
    $scope.patientNotFound = patientNotFound;
    $scope.recruit = recruit;

    $scope.backToSearch = backToSearch;
    $scope.backToResults = backToResults;

    function search() {
      $scope.loading = true;

      adapter.post('/recruit-patient-search', {}, $scope.searchParams)
        .then(function(response) {
          var results = response.data.results;

          $scope.results = results;
          $scope.searchErrors = {};

          if (results.length) {
            $state.go('recruitPatient.results');
          } else {
            $scope.patientNotFound();
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
    }

    function patientFound(result) {
      $scope.patient = {
        mpiid: result.mpiid,
        radarId: result.radarId,
        firstName: result.firstName,
        lastName: result.lastName,
        dateOfBirth: result.dateOfBirth,
        nhsNo: result.nhsNo,
        chiNo: result.chiNo
      };

      $state.go('recruitPatient.form');
    }

    function patientNotFound() {
      $scope.patient = {
        firstName: $scope.searchParams.firstName,
        lastName: $scope.searchParams.lastName,
        dateOfBirth: $scope.searchParams.dateOfBirth
      };

      $state.go('recruitPatient.form');
    }

    function recruit() {
      $scope.loading = true;

      adapter.post('/recruit-patient', {}, $scope.patient)
        .then(function(response) {
          var patientId = response.data.id;
          $state.go('patient.demographics', {patientId: patientId});
        })
        ['catch'](function(response) {
          if (response.status === 422) {
            $scope.patientErrors = response.data.errors || {};
          }
        })
        ['finally'](function() {
          $scope.loading = false;
        });
    }

    function backToSearch() {
      $state.go('recruitPatient.search');
    }

    function backToResults() {
      $state.go('recruitPatient.results');
    }
  }

  RecruitPatientController.$inject = [
    '$scope',
    'adapter',
    '$state',
    '$q',
    'store'
  ];

  app.controller('RecruitPatientController', RecruitPatientController);
})();
