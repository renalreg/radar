(function() {
  'use strict';

  var app = angular.module('radar.utils');

  app.factory('transformKeys', ['_', function(_) {
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
  }]);

  app.factory('camelCaseKeys', ['transformKeys', '_', function(transformKeys, _) {
    var re = new RegExp('^[A-Z0-9_]+$');

    return function camelCaseObject(x) {
      return transformKeys(x, function(key) {
        if (re.exec(key)) {
          return key;
        } else {
          return _.camelCase(key);
        }
      });
    };
  }]);

  app.factory('snakeCaseKeys', ['transformKeys', '_', function(transformKeys, _) {
    var re = new RegExp('^[A-Z0-9_]+$');

    return function snakeCaseObject(x) {
      return transformKeys(x, function(key) {
        if (re.exec(key)) {
          return key;
        } else {
          return _.snakeCase(key);
        }
      });
    };
  }]);
})();
