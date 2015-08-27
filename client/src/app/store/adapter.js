(function() {
  'use strict';

  var app = angular.module('radar.store');

  app.provider('adapter', function() {
    var config = {
      baseUrl: ''
    };

    this.setBaseUrl = function(value) {
      config.baseUrl = value;
    };

    this.$get = function($http, $q, _, camelCaseKeys, snakeCaseKeys, flattenRelationships) {
      function Adapter(config) {
        this.config = config;
      }

      Adapter.prototype.getUrl = function(url) {
        return this.config.baseUrl + url;
      };

      Adapter.prototype.getModelUrl = function(name, id) {
        if (id === undefined) {
          return '/' + name;
        } else {
          return '/' + name + '/' + id;
        }
      };

      Adapter.prototype.transformRequest = function(data) {
        data = snakeCaseKeys(data);
        data = flattenRelationships(data);
        return data;
      };

      Adapter.prototype.transformParams = function(data) {
        return snakeCaseKeys(data);
      };

      Adapter.prototype.transformResponse = function(data) {
        return camelCaseKeys(data);
      };

      Adapter.prototype.findOne = function(name, id) {
        var self = this;

        var url = self.getModelUrl(name, id);

        self.logModelRequest(name, 'GET', url);

        return self.get(url)
          .then(function(response) {
            return response.data;
          })
          .catch(function(response) {
            var data = {status: response.status};
            return $q.reject(data);
          });
      };

      Adapter.prototype.findMany = function(name, params) {
        var self = this;

        var url = self.getModelUrl(name);

        self.logModelRequest(name, 'GET', url);

        return self.get(url, params)
          .then(function(response) {
            return response.data.data;
          })
          .catch(function(response) {
            var data = {status: response.status};
            return $q.reject(data);
          });
      };

      Adapter.prototype.create = function(name, data) {
        var self = this;

        var url = self.getModelUrl(name);

        self.logModelRequest(name, 'POST', url);

        return self.post(url, {}, data)
          .then(function(response) {
            return response.data;
          })
          .catch(function(response) {
            var data = {status: response.status};

            if (response.status === 422) {
              data.errors = self.transformResponse(response.data.errors);
            }

            return $q.reject(data);
          });
      };

      Adapter.prototype.update = function(name, id, data) {
        var self = this;

        var url = self.getModelUrl(name, id);

        self.logModelRequest(name, 'PUT', url);

        return self.put(url, {}, data)
          .then(function(response) {
            return response.data;
          })
          .catch(function(response) {
            var data = {status: response.status};

            if (response.status === 422) {
              data.errors = response.data.errors;
            }

            return $q.reject(data);
          });
      };

      Adapter.prototype.remove = function(name, id) {
        var self = this;

        var url = self.getModelUrl(name, id);

        self.logModelRequest(name, 'DELETE', url);

        return self.delete(url)
          .then(function() {
            return undefined;
          })
          .catch(function(response) {
            var data = {status: response.status};
            return $q.reject(data);
          });
      };

      Adapter.prototype.get = function(url, params) {
        return this.request('GET', url, params);
      };

      Adapter.prototype.post = function(url, params, data) {
        return this.request('POST', url, params, data);
      };

      Adapter.prototype.put = function(url, params, data) {
        return this.request('PUT', url, params, data);
      };

      Adapter.prototype.delete = function(url, params) {
        return this.request('DELETE', url, params);
      };

      Adapter.prototype.request = function(method, url, params, data) {
        var self = this;

        var config = {};

        config.method = method;
        config.url = self.getUrl(url);

        if (params) {
          config.params = self.transformParams(params);
        }

        if (data) {
          config.data = self.transformRequest(data);
        }

        return $http(config)
          .then(function(response) {
            if (angular.isObject(response.data)) {
              response.data = self.transformResponse(response.data);
            }

            return response;
          })
          .catch(function(response) {
            if (angular.isObject(response.data)) {
              response.data = self.transformResponse(response.data);
            }

            return $q.reject(response);
          });
      };

      Adapter.prototype.logModelRequest = function(name, method, url) {
        console.log('[' + name + '] ' + method + ' ' + url);
      };

      return new Adapter(config);
    };
  });
})();
