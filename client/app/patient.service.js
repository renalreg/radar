(function() {
  'use strict';

  var app = angular.module('radar');

  app.factory('PatientService', function($resource) {
    return $resource(
      'http://localhost:5000/patients/:id',
      {},
      {
        'query': {
          method: 'GET',
          isArray: true,
          transformResponse: function(data) {
            return angular.fromJson(data).data;
          }
        }
      }
    );
  });
})();
