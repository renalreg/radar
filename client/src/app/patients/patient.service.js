(function() {
  'use strict';

  var app = angular.module('radar.patients');

  app.factory('PatientService', function(endpointFactory) {
    var Endpoint = endpointFactory('/patients/:id', {
      params: {
        id: '@id'
      }
    });

    return {
      getPatient: getPatient,
      getPatients: getPatients
    };

    function getPatient(id) {
      console.log(id);
      return Endpoint.get({id: id}).$promise;
    }

    function getPatients() {
      return Endpoint.query().$promise;
    }
  });
})();
