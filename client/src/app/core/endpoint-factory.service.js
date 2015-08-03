/* globals humps, _ */

(function() {
  'use strict';

  var app = angular.module('radar.core');

  app.factory('flattenRelationships', function() {
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

  app.factory('ensureArray', function() {
    return function ensureArray(value) {
      return angular.isArray(value) ? value : [value];
    };
  });

  app.factory('endpointFactory', function($resource, $http, ensureArray, flattenRelationships) {
    var defaultTransformRequest = ensureArray($http.defaults.transformRequest);
    var defaultTransformResponse = ensureArray($http.defaults.transformResponse);

    function endpointFactory(url, options) {
      var resourceParams;

      if (angular.isDefined(options)) {
        resourceParams = options.params || {};
      } else {
        resourceParams = {};
      }

      var resourceActions = {
        get: {
          method: 'GET'
        },
        save: {
          method: 'POST'
        },
        query: {
          method: 'GET',
          isArray: true
        },
        remove: {
          method: 'DELETE'
        },
        delete: {
          method: 'DELETE'
        }
      };

      _.each(resourceActions, function(action) {
        var transformRequest = function(data) {
          data = flattenRelationships(data);
          data = humps.decamelizeKeys(data);

          return data;
        };

        action.transformRequest = [transformRequest]
          .concat(defaultTransformRequest);

        var transformResponse = function(data) {
          data = angular.fromJson(data);

          if (angular.isDefined(data.data)) {
            data = data.data;
          }

          data = humps.camelizeKeys(data);

          return data;
        };

        action.transformResponse = defaultTransformResponse
          .concat(transformResponse);
      });

      // TODO add to config
      var resourceUrl = 'http://localhost:5000' + url;

      return $resource(resourceUrl, resourceParams, resourceActions);
    }

    return endpointFactory;
  });
})();
