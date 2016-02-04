(function() {
  'use strict';

  var app = angular.module('radar.recruitPatient');

  function RecruitPatientController(
    $scope,
    adapter,
    $state,
    $q,
    store,
    _
  ) {
    $scope.loading = true;

    $scope.searchParams = {};
    $scope.searchErrors = {};

    $scope.patient = {};
    $scope.patientErrors = {};

    $scope.search = search;
    $scope.patientFound = patientFound;
    $scope.patientNotFound = patientNotFound;
    $scope.recruit = recruit;

    $scope.backToSearch = backToSearch;

    init();

    function init() {
      $q.all([loadGenders(), loadEthnicities(), loadNumberGroups()]).then(function() {
        $scope.loading = false;
      });
    }

    function search() {
      $scope.loading = true;

      return adapter.post('/recruit-patient-search', {}, $scope.searchParams)
        .then(function(response) {
          var patients = response.data.patients;

          $scope.patients = patients;
          $scope.searchErrors = {};

          if (patients.length) {
            patientFound(patients[0]);
          } else {
            patientNotFound();
          }

          $state.go('recruitPatient.form');
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

    function patientFound(patient) {
      $scope.patient = {
        existing: true,
        firstName: patient.firstName,
        lastName: patient.lastName,
        dateOfBirth: patient.dateOfBirth,
        gender: patient.gender,
        patientNumbers: patient.patientNumbers
      };
    }

    function patientNotFound() {
      $scope.patient = {
        existing: false,
        firstName: $scope.searchParams.firstName,
        lastName: $scope.searchParams.lastName,
        dateOfBirth: $scope.searchParams.dateOfBirth,
        patientNumbers: [
          {
            number: $scope.searchParams.number,
            numberGroup: $scope.searchParams.numberGroup
          }
        ]
      };
    }

    function recruit() {
      $scope.loading = true;

      return adapter.post('/recruit-patient', {}, $scope.patient)
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

    function loadGenders() {
      return store.findMany('genders').then(function(genders) {
        $scope.genders = genders;
      });
    }

    function loadEthnicities() {
      return store.findMany('ethnicities').then(function(ethnicities) {
        $scope.ethnicities = ethnicities;
      });
    }

    function loadNumberGroups() {
      return store.findMany('groups', {isRecruitmentNumberGroup: true}).then(function(groups) {
        // Sort by name
        groups = _.sortBy(groups, 'name');

        // Set the options
        $scope.numberGroups = groups;
      });
    }
  }

  RecruitPatientController.$inject = [
    '$scope',
    'adapter',
    '$state',
    '$q',
    'store',
    '_'
  ];

  app.controller('RecruitPatientController', RecruitPatientController);
})();
