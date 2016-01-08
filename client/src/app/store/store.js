(function() {
  'use strict';

  var app = angular.module('radar.store');

  app.provider('store', function() {
    var config = {
      models: {},
      childModels: {}
    };

    this.registerModel = function(name, constructorName) {
      config.models[name] = constructorName;
    };

    this.registerChildModel = function(key, name) {
      config.childModels[key] = name;
    };

    this.$get = ['_', '$injector', 'adapter', '$q', function(_, $injector, adapter, $q) {
      function Store(config) {
        this.config = config;
        this.store = {};
        this.pristineStore = {};
        this.eventListeners = {};
        this.modelEventListeners = {};
      }

      Store.prototype.getModelConstructor = function(modelName) {
        var modelConstructorName = this.config.models[modelName] || 'Model';
        return $injector.get(modelConstructorName);
      };

      Store.prototype.create = function(modelName, data) {
        if (data === undefined) {
          data = {};
        }

        var Model = this.getModelConstructor(modelName);
        data = this.inflate(data);
        return new Model(modelName, data);
      };

      Store.prototype.getStore = function(modelName) {
        if (this.store[modelName] === undefined) {
          this.store[modelName] = {};
        }

        return this.store[modelName];
      };

      Store.prototype.getFromStore = function(modelName, id) {
        var store = this.getStore(modelName);
        return store[id] || null;
      };

      Store.prototype.getPristineStore = function(modelName) {
        if (this.pristineStore[modelName] === undefined) {
          this.pristineStore[modelName] = {};
        }

        return this.pristineStore[modelName];
      };

      Store.prototype.getFromPristineStore = function(modelName, id) {
        var store = this.getPristineStore(modelName);
        return store[id] || null;
      };

      Store.prototype.pushToStore = function(item) {
        var modelName = item.modelName;
        var id = item.getId();

        var pristineStore = this.getPristineStore(modelName);
        var pristineItem = angular.copy(item);
        pristineStore[id] = pristineItem;

        var existingItem = this.getFromStore(modelName, id);

        if (existingItem === null) {
          var store = this.getStore(modelName);
          store[id] = item;
          return item;
        } else {
          existingItem.update(item.getData());
          return existingItem;
        }
      };

      Store.prototype.isPristine = function(item) {
        var modelName = item.modelName;
        var id = item.getId();

        var pristineItem = this.getFromPristineStore(modelName, id);

        return pristineItem !== null && angular.equals(item.getData(), pristineItem.getData());
      };

      Store.prototype.isDirty = function(item) {
        return !this.isPristine(item);
      };

      Store.prototype.findOne = function(modelName, id, useCache) {
        if (useCache === undefined) {
          useCache = false;
        }

        var self = this;
        var Model = self.getModelConstructor(modelName);

        var existingItem = self.getFromStore(modelName, id);

        // Return cached value
        if (useCache && existingItem !== null) {
          var deferred = $q.defer();
          deferred.resolve(existingItem);
          return deferred.promise;
        }

        if (existingItem !== null) {
          existingItem.isLoading = true;
        }

        var promise = adapter.findOne(modelName, id).then(function(data) {
          data = self.inflate(data);
          return self.pushToStore(new Model(modelName, data));
        });

        if (existingItem !== null) {
          promise = promise['finally'](function() {
            existingItem.isLoading = false;
          });
        }

        return promise;
      };

      Store.prototype.findMany = function(modelName, params, meta) {
        var self = this;
        var Model = self.getModelConstructor(modelName);

        params = params || {};

        return adapter.findMany(modelName, params, meta).then(function(data) {
          var items = [];
          var r;
          var rawItems;

          if (meta) {
            rawItems = data.data;
            r = {
              data: items,
              pagination: data.pagination
            };
          } else {
            rawItems = data;
            r = items;
          }

          for (var i = 0; i < rawItems.length; i++) {
            var rawItem = rawItems[i];
            var inflatedItem = self.inflate(rawItem);
            var item = self.pushToStore(new Model(modelName, inflatedItem));
            items.push(item);
          }

          return r;
        });
      };

      Store.prototype.findFirst = function(modelName, params) {
        return this.findMany(modelName, params).then(function(items) {
          if (items.length) {
            return items[0];
          } else {
            return null;
          }
        });
      };

      Store.prototype.save = function(item) {
        var self = this;
        var id = item.getId();
        var modelName = item.modelName;
        var data = item.getData();
        var Model = self.getModelConstructor(modelName);
        var promise;
        var create = id === null;

        item.isSaving = true;

        if (create) {
          promise = adapter.create(modelName, data);
        } else {
          var existingItem = self.getFromStore(modelName, id);
          var copy = existingItem !== null && existingItem !== item;

          if (copy) {
            existingItem.isSaving = true;
          }

          promise = adapter.update(modelName, id, data);

          if (copy) {
            promise = promise['finally'](function() {
              existingItem.isSaving = false;
            });
          }
        }

        promise = promise.then(function(data) {
          item.isValid = true;
          item.isError = false;
          item.errors = {};
          data = self.inflate(data);
          var savedItem = new Model(modelName, data).getData();
          item.update(savedItem);
          return self.pushToStore(item);
        });

        promise = promise['catch'](function(data) {
          if (data.status === 422) {
            item.isValid = false;
            item.errors = data.errors;
          } else {
            item.isError = true;
          }

          return $q.reject(data);
        });

        promise = promise['finally'](function() {
          item.isSaving = false;
        });

        return promise;
      };

      Store.prototype.remove = function(obj) {
        var id = obj.getId();
        var modelName = obj.modelName;

        obj.isSaving = true;
        obj.isDeleted = true;

        return adapter.remove(modelName, id)
          ['catch'](function() {
            obj.isDeleted = false;
          })
          ['finally'](function() {
            obj.isSaving = false;
          });
      };

      Store.prototype.addEventListener = function(event, callback) {
        if (this.eventListeners[event] === undefined) {
          this.eventListeners[event] = [];
        }

        this.eventListeners[event].push(callback);
      };

      Store.prototype.getEventListeners = function(event) {
        return this.eventListeners[event] || [];
      };

      Store.prototype.addModelEventListener = function(modelName, event, callback) {
        if (this.modelEventListeners[modelName] === undefined) {
          this.modelEventListeners[modelName] = {};
        }

        if (this.modelEventListeners[modelName][event] === undefined) {
          this.modelEventListeners[modelName][event] = [];
        }

        this.modelEventListeners[modelName][event].push(callback);
      };

      Store.prototype.getModelEventListeners = function(modelName, event) {
        if (this.modelEventListeners[modelName] === undefined) {
          return [];
        }

        return this.modelEventListeners[modelName][event] || [];
      };

      Store.prototype.getListeners = function(modelName, event) {
        var listeners = this.getEventListeners(event);
        return listeners.concat(this.getModelEventListeners(modelName, event));
      };

      Store.prototype.broadcast = function(modelName, event) {
        var args = Array.prototype.slice.call(1, arguments);
        var listeners = this.getListeners(modelName, event);

        _.forEach(listeners, function(listener) {
          listener(args);
        });
      };

      Store.prototype.on = function(modelName, event, callback) {
        if (callback === undefined) {
          callback = event;
          event = modelName;
          modelName = null;
        }

        if (modelName === null) {
          this.addEventListener(event, callback);
        } else {
          this.addModelEventListener(modelName, event, callback);
        }
      };

      Store.prototype.inflate = function(data) {
        var self = this;

        if (angular.isArray(data)) {
          return _.map(data, function(value) {
            return self.inflate(value);
          });
        } else if (angular.isObject(data)) {
          return _.mapValues(data, function(value, key) {
            value = self.inflate(value);

            var modelName = self.config.childModels[key];

            if (modelName !== undefined) {
              var Model = self.getModelConstructor(modelName);

              if (angular.isArray(value)) {
                value = _.map(value, function(x) {
                  return self.pushToStore(new Model(modelName, x));
                });
              } else {
                value = self.pushToStore(new Model(modelName, value));
              }
            }

            return value;
          });
        } else {
          return data;
        }
      };

      return new Store(config);
    }];
  });
})();
