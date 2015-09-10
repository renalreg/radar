(function() {
  'use strict';

  var app = angular.module('radar.utils');

  app.factory('firstPromise', function($q) {
    return function firstPromise(promises) {
      if (promises.length) {
        var promise = promises[0];

        return $q.all(promises).then(function() {
          return promise;
        });
      } else {
        var deferred = $q.defer();
        deferred.resolve();
        return deferred.promise;
      }
    };
  });
})();
