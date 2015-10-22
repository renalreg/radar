(function() {
  'use strict';

  var app = angular.module('radar.utils');

  app.factory('flattenRelationships', ['_', function(_) {
    return function flattenRelationships(data, depth) {
      if (depth === undefined) {
        depth = 0;
      }

      var newData;

      if (angular.isArray(data)) {
        newData = [];

        _.each(data, function(value) {
          newData.push(flattenRelationships(value, depth + 1));
        });
      } else if (angular.isObject(data)) {
        if (depth > 0 && data.id !== undefined) {
          newData = data.id;
        } else {
          newData = {};

          _.each(data, function(value, key) {
            newData[key] = flattenRelationships(value, depth + 1);
          })
        }
      } else {
        newData = data;
      }

      return newData;
    };
  }]);
})();
