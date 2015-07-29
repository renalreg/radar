(function() {
  'use strict';

  var app = angular.module('radar.patient');

  app.factory('PatientService', function(Restangular) {
    return {
      getPatients: getPatients,
      getPatient: getPatient
    };

    function getPatient(id) {
      return Restangular.one('patients', id).get();
    }

    function getPatients() {
      return Restangular.all('patients').getList();
    }
  });
})();
