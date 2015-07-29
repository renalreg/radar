(function() {
  'use strict';

  var app = angular.module('radar');

  app.factory('PatientService', function(Restangular) {
    return {
      getPatients: getPatients
    };

    function getPatients() {
      return Restangular.all('patients').getList();
    }
  });
})();
