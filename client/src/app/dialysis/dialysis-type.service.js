(function() {
  'use strict';

  var app = angular.module('radar');

  app.factory('DialysisTypeService', function(endpointFactory) {
    var endpoint = endpointFactory('/dialysis-types');

    return {
      getDialysisTypes: getDialysisTypes
    };

    function getDialysisTypes() {
      return endpoint.query().$promise;
    }
  });
})();
