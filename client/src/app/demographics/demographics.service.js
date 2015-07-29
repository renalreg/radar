(function() {
  'use strict';

  var app = angular.module('radar.demographics');

  app.factory('DemographicsService', function(Restangular) {
    return {
      getList: getList
    };

    function getList(patientId) {
      return Restangular.all('demographics').getList({patientId: patientId});
    }
  });
})();
