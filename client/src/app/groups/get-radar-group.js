(function() {
  'use strict';

  var app = angular.module('radar.groups');

  app.factory('getRadarGroup', ['store', '$q', function(store, $q) {
    var deferred = null;

    function getRadarGroup() {
      if (deferred === null) {
        deferred = $q.defer();

        var params = {
          code: 'RADAR',
          type: 'OTHER'
        };

        store.findFirst('groups', params)
          .then(function(group) {
            deferred.resolve(group);
          })
          ['catch'](function() {
            deferred.reject();
          });
      }

      return deferred.promise;
    }

    return getRadarGroup;
  }]);
})();
