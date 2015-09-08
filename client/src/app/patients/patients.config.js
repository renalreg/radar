(function() {
  'use strict';

  var app = angular.module('radar.patients');

  app.config(function($stateProvider) {
    $stateProvider.state('patients', {
      url: '/patients',
      templateUrl: 'app/patients/patient-list.html',
      controller: function($scope, $controller, PatientListController) {
        $controller(PatientListController, {$scope: $scope});
      }
    });

    $stateProvider.state('patient', {
      url: '/patients/:patientId',
      abstract: true,
      templateUrl: 'app/patients/patient-detail.html',
      controller: 'PatientDetailController',
      resolve: {
        patient: function($stateParams, store) {
          return store.findOne('patients', $stateParams.patientId);
        }
      }
    });
  });

  app.constant('patientFeatures', {
    DEMOGRAPHICS: {
      text: 'Demographics',
      url: 'patient.demographics({patientId: patient.id})'
    },
    DIALYSIS: {
      text: 'Dialysis',
      url: 'patient.dialysis({patientId: patient.id})'
    },
    DISEASE_GROUPS: {
      text: 'Disease Groups',
      url: 'patient.diseaseGroups({patientId: patient.id})'
    },
    HOSPITALISATIONS: {
      text: 'Hospitalisations',
      url: 'patient.hospitalisations({patientId: patient.id})'
    },
    MEDICATIONS: {
      text: 'Medications',
      url: 'patient.medications({patientId: patient.id})'
    },
    PLASMAPHERESIS: {
      text: 'Plasmapheresis',
      url: 'patient.plasmapheresis({patientId: patient.id})'
    },
    UNITS: {
      text: 'Units',
      url: 'patient.units({patientId: patient.id})'
    }
  });

  app.constant('radarPatientFeatures', [
    'DEMOGRAPHICS',
    'MEDICATIONS',
    'HOSPITALISATIONS',
    'DIALYSIS',
    'PLASMAPHERESIS',
    'DISEASE_GROUPS',
    'UNITS'
  ]);
})();
