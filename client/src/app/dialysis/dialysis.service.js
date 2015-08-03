(function() {
  'use strict';

  var app = angular.module('radar.dialysis');

  app.factory('DialysisService', function(endpointFactory) {
    var Endpoint = endpointFactory('/dialysis/:id', {
      params: {
        'id': '@id'
      }
    });

    return {
      getList: getList,
      create: create
    };

    function create(data) {
      return new Endpoint(data);
    }

    function getList(patientId) {
      return Endpoint.query({patientId: patientId}).$promise;
    }
  });
})();
