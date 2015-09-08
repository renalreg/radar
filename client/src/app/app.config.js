(function() {
  'use strict';

  var app = angular.module('radar');

  app.config(function($httpProvider) {
    $httpProvider.interceptors.push('unauthorizedHttpInterceptor');
    $httpProvider.interceptors.push('xAuthTokenHttpInterceptor');
  });

  app.config(function($stateProvider, $urlRouterProvider) {
    $urlRouterProvider.otherwise('/');
  });

  app.config(function(adapterProvider) {
    adapterProvider.setBaseUrl('http://localhost:5000');
  });

  app.config(function($stateProvider) {
    $stateProvider.state('index', {
      url: '/',
      templateUrl: 'app/core/index.html'
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
    MEDICATIONS: {
      text: 'Medications',
      url: 'patient.medications({patientId: patient.id})'
    },
    UNITS: {
      text: 'Units',
      url: 'patient.units({patientId: patient.id})'
    }
  });

  app.constant('radarPatientFeatures', [
    'DEMOGRAPHICS',
    'MEDICATIONS',
    'DIALYSIS',
    'DISEASE_GROUPS',
    'UNITS'
  ]);
})();
