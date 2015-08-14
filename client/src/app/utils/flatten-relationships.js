(function() {
  'use strict';

  var app = angular.module('radar.utils');

  app.factory('flattenRelationships', function(_) {
    return function flattenRelationships(data) {
      var newData;

      if (angular.isArray(data)) {
        newData = [];

        _.each(data, function(value) {
          if (angular.isObject(value)) {
            newData.push(flattenRelationships(value));
          } else {
            newData.push(value);
          }
        });
      } else if (angular.isObject(data)) {
        newData = {};

        _.each(data, function(value, key) {
          if (angular.isArray(value)) {
            newData[key] = flattenRelationships(value);
          } else if (angular.isObject(value)) {
            if (value.id !== undefined) {
              newData[key + 'Id'] = value.id;
            } else {
              newData[key] = flattenRelationships(value);
            }
          } else {
            newData[key] = value;
          }
        });
      } else {
        newData = data;
      }

      return newData;
    };
  });
})();
