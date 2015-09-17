(function() {
  'use strict';

  var app = angular.module('radar.patients');

  app.factory('getRadarDataSource', function(store, $q) {
    var deferred = null;

    function getRadarDataSource() {
      if (deferred === null) {
        deferred = $q.defer();

        var params = {
          organisationCode: 'RADAR',
          organisationType: 'OTHER',
          type: 'RADAR'
        };

        store.findMany('data-sources', params)
          .then(function(dataSources) {
            deferred.resolve(dataSources[0]);
          })
          .catch(function() {
            deferred.reject();
          });
      }

      return deferred.promise;
    }

    return getRadarDataSource;
  });
})();
