(function() {
  'use strict';

  var app = angular.module('radar');

  app.factory('DialysisService', function(Restangular) {
    return {
      getList: getList
    };

    function getList(patientId) {
      return Restangular.all('dialysis').getList({patientId: patientId});
    }
  });
})();
