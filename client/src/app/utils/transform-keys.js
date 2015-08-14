(function() {
  'use strict';

  var app = angular.module('radar.utils');

  app.factory('transformKeys', function(_) {
    return function transformKeys(x, f) {
      if (_.isArray(x)) {
        return _.map(x, function(value) {
          return transformKeys(value, f);
        });
      } else if (_.isObject(x)) {
        return _.transform(x, function(result, value, key) {
          result[f(key)] = transformKeys(value, f);
        });
      } else {
        return x;
      }
    };
  });

  app.factory('camelCaseKeys', function(transformKeys, _) {
    return function camelCaseObject(x) {
      return transformKeys(x, function(key) {
        return _.camelCase(key);
      });
    };
  });

  app.factory('snakeCaseKeys', function(transformKeys, _) {
    return function snakeCaseObject(x) {
      return transformKeys(x, function(key) {
        return _.snakeCase(key);
      });
    };
  });
})();
