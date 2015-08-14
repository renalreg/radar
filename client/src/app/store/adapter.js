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

      Adapter.prototype.getUrl = function(name, id) {
        if (id === undefined) {
          return this.config.baseUrl + '/' + name;
        } else {
          return this.config.baseUrl + '/' + name + '/' + id;
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

      Adapter.prototype.transformErrors = function(data) {
        return camelCaseKeys(data);
      };

      Adapter.prototype.get = function(name, id) {
        var self = this;
        var url = self.getUrl(name, id);

        self.logRequest(name, 'GET', url);

        return $http.get(url)
          .then(function(response) {
            return self.transformResponse(response.data);
          })
          .catch(function(response) {
            var data = {status: response.status};
            return $q.reject(data);
          });
      };

      Adapter.prototype.query = function(name, params) {
        var self = this;
        var url = self.getUrl(name);

        params = self.transformParams(params);

        self.logRequest(name, 'GET', url);

        return $http.get(url, {params: params})
          .then(function(response) {
            return self.transformResponse(response.data.data);
          })
          .catch(function(response) {
            var data = {status: response.status};
            return $q.reject(data);
          });
      };

      Adapter.prototype.create = function(name, data) {
        var self = this;
        var url = self.getUrl(name);

        data = self.transformRequest(data);

        self.logRequest(name, 'POST', url);

        return $http.post(url, data)
          .then(function(response) {
            return self.transformResponse(response.data);
          })
          .catch(function(response) {
            var data = {status: response.status};

            if (response.status === 422) {
              data.errors = self.transformErrors(response.data.errors);
            }

            return $q.reject(data);
          });
      };

      Adapter.prototype.update = function(name, id, data) {
        var self = this;
        var url = self.getUrl(name, id);

        data = self.transformRequest(data);

        self.logRequest(name, 'PUT', url);

        return $http.put(url, data)
          .then(function(response) {
            return self.transformResponse(response.data);
          })
          .catch(function(response) {
            var data = {status: response.status};

            if (response.status === 422) {
              data.errors = self.transformErrors(response.data.errors);
            }

            return $q.reject(data);
          });
      };

      Adapter.prototype.remove = function(name, id) {
        var self = this;
        var url = self.getUrl(name, id);

        self.logRequest(name, 'DELETE', url);

        return $http.delete(url)
          .then(function() {
            return undefined;
          })
          .catch(function(response) {
            var data = {status: response.status};
            return $q.reject(data);
          });
      };

      Adapter.prototype.logRequest = function(name, method, url) {
        console.log('[' + name + '] ' + method + ' ' + url);
      };

      return new Adapter(config);
    };
  });
})();
