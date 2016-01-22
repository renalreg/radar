(function() {
  'use strict';

  var app = angular.module('radar.store');

  app.provider('adapter', function() {
    var config = {
      baseUrl: '',
      beforeRequestChain: [],
      afterResponseChain: []
    };

    this.setBaseUrl = function(value) {
      config.baseUrl = value;
    };

    this.beforeRequest = function(name) {
      config.beforeRequestChain.push(name);
    };

    this.afterResponse = function(name) {
      config.afterResponseChain.push(name);
    };

    this.$get = function($http, $q, _, camelCaseKeys, snakeCaseKeys, flattenRelationships, $injector) {
      function Adapter(config) {
        this.config = config;

        this.baseUrl = config.baseUrl;

        this.beforeRequestChain = null;
        this.afterResponseChain = null;
      }

      Adapter.prototype.getUrl = function(url) {
        return this.baseUrl + url;
      };

      Adapter.prototype.getBeforeRequestChain = function() {
        if (this.beforeRequestChain === null) {
          this.beforeRequestChain = _.map(this.config.beforeRequestChain, function(name) {
            return $injector.get(name);
          });
        }

        return this.beforeRequestChain;
      };

      Adapter.prototype.getAfterResponseChain = function() {
        if (this.afterResponseChain === null) {
          this.afterResponseChain = _.map(this.config.afterResponseChain, function(name) {
            return $injector.get(name);
          });
        }

        return this.afterResponseChain;
      };

      Adapter.prototype.getModelUrl = function(modelName, id) {
        if (id === undefined) {
          return '/' + modelName;
        } else {
          return '/' + modelName + '/' + id;
        }
      };

      Adapter.prototype.transformRequest = function(data) {
        data = flattenRelationships(data);
        data = snakeCaseKeys(data);
        return data;
      };

      Adapter.prototype.transformParams = function(data) {
        data = flattenRelationships(data);
        data = snakeCaseKeys(data);

        if (data.sort) {
          if (/^-/.exec(data.sort)) {
            data.sort = '-' + _.snakeCase(data.sort);
          } else {
            data.sort = _.snakeCase(data.sort);
          }
        }

        return data;
      };

      Adapter.prototype.transformResponse = function(data) {
        return camelCaseKeys(data);
      };

      Adapter.prototype.findOne = function(modelName, id) {
        var self = this;

        var url = self.getModelUrl(modelName, id);

        return self.get(url)
          .then(function(response) {
            return response.data;
          })
          ['catch'](function(response) {
            var data = {status: response.status};
            return $q.reject(data);
          });
      };

      Adapter.prototype.findMany = function(modelName, params, meta) {
        var self = this;

        var url = self.getModelUrl(modelName);

        return self.get(url, params)
          .then(function(response) {
            if (meta) {
              return response.data;
            } else {
              return response.data.data;
            }
          })
          ['catch'](function(response) {
            var data = {status: response.status};
            return $q.reject(data);
          });
      };

      Adapter.prototype.create = function(modelName, data) {
        var self = this;

        var url = self.getModelUrl(modelName);

        return self.post(url, {}, data)
          .then(function(response) {
            return response.data;
          })
          ['catch'](function(response) {
            var data = {status: response.status};

            if (response.status === 422) {
              data.errors = self.transformResponse(response.data.errors);
            }

            return $q.reject(data);
          });
      };

      Adapter.prototype.update = function(modelName, id, data) {
        var self = this;

        var url = self.getModelUrl(modelName, id);

        return self.put(url, {}, data)
          .then(function(response) {
            return response.data;
          })
          ['catch'](function(response) {
            var data = {status: response.status};

            if (response.status === 422) {
              data.errors = response.data.errors;
            }

            return $q.reject(data);
          });
      };

      Adapter.prototype.remove = function(modelName, id) {
        var self = this;

        var url = self.getModelUrl(modelName, id);

        return self['delete'](url)
          .then(function() {
            return undefined;
          })
          ['catch'](function(response) {
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

      Adapter.prototype['delete'] = function(url, params) {
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

        // Apply before request chain
        _.forEach(this.getBeforeRequestChain(), function(beforeRequest) {
          config = beforeRequest(config);
        });

        var promise = $http(config)
          .then(function(response) {
            if (angular.isObject(response.data)) {
              response.data = self.transformResponse(response.data);
            }

            return response;
          })
          ['catch'](function(response) {
            if (angular.isObject(response.data)) {
              response.data = self.transformResponse(response.data);
            }

            return $q.reject(response);
          });

        // Apply after response chain
        _.forEach(this.getAfterResponseChain(), function(afterResponse) {
          promise = afterResponse(promise);
        });

        return promise;
      };

      return new Adapter(config);
    };

    this.$get.$inject = [
      '$http', '$q', '_', 'camelCaseKeys', 'snakeCaseKeys', 'flattenRelationships', '$injector'
    ];
  });
})();
