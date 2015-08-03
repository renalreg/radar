(function() {
  'use strict';

  var app = angular.module('radar.demographics');

  app.factory('DemographicsService', function(endpointFactory) {
    var Endpoint = endpointFactory('/demographics/:id', {
      params: {
        id: '@id'
      }
    });

    return {
      getList: getList
    };

    function getList(patientId) {
      return Endpoint.query({patientId: patientId});
    }
  });
})();
