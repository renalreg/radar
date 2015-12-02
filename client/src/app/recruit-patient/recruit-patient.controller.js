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
    $scope.backToResults = backToResults;

    init();

    function init() {
      $q.all([loadGenders(), loadEthnicityCodes(), loadNumberOrganisations()]).then(function() {
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
            $state.go('recruitPatient.results');
          } else {
            patientNotFound();
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

    function patientFound(patient) {
      $scope.patient = {
        firstName: patient.firstName,
        lastName: patient.lastName,
        dateOfBirth: patient.dateOfBirth,
        gender: patient.gender,
        patientNumbers: patient.patientNumbers
      };

      $state.go('recruitPatient.form');
    }

    function patientNotFound() {
      $scope.patient = {
        firstName: $scope.searchParams.firstName,
        lastName: $scope.searchParams.lastName,
        dateOfBirth: $scope.searchParams.dateOfBirth,
        patientNumbers: [
          {
            number: $scope.searchParams.number,
            organisation: $scope.searchParams.numberOrganisation
          }
        ]
      };

      $state.go('recruitPatient.form');
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

    function backToResults() {
      $state.go('recruitPatient.results');
    }

    function loadGenders() {
      return store.findMany('genders').then(function(genders) {
        $scope.genders = genders;
      });
    }

    function loadEthnicityCodes() {
      return store.findMany('ethnicity-codes').then(function(ethnicityCodes) {
        $scope.ethnicityCodes = ethnicityCodes;
      });
    }

    function loadNumberOrganisations() {
      return store.findMany('organisations', {isNational: true}).then(function(organisations) {
        // Sort by name
        organisations = _.sortBy(organisations, 'name');

        // Default to a NHS number
        $scope.searchParams.numberOrganisation = _.find(organisations, function(x) {
          return x.code === 'NHS' && x.type === 'OTHER';
        });

        // Set the options
        $scope.numberOrganisations = organisations;
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
