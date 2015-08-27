(function() {
  'use strict';

  var app = angular.module('radar.store');

  app.provider('store', function() {
    var config = {
      models: {}
    };

    this.registerModel = function(name, modelName) {
      config.models[name] = modelName;
    };

    this.$get = function(_, $injector, adapter, $q) {
      function Store(config) {
        this.config = config;
        this.store = {};
        this.eventListeners = {};
        this.modelEventListeners = {};
      }

      Store.prototype.getModel = function(name) {
        var modelName = this.config.models[name] || 'Model';
        return $injector.get(modelName);
      };

      Store.prototype.create = function(name, data) {
        var Model = this.getModel(name);
        return new Model(name, data);
      };

      Store.prototype.getStore = function(name) {
        if (this.store[name] === undefined) {
          this.store[name] = {};
        }

        return this.store[name];
      };

      Store.prototype.getFromStore = function(name, id) {
        var store = this.getStore(name);
        return store[id] || null;
      };

      Store.prototype.pushToStore = function(item) {
        var name = item.name;
        var id = item.getId();

        var existingItem = this.getFromStore(name, id);

        if (existingItem === null) {
          var store = this.getStore(name);
          store[id] = item;
          return item;
        } else {
          existingItem.update(item.getData());
          return existingItem;
        }
      };

      Store.prototype.findOne = function(name, id) {
        var self = this;
        var Model = self.getModel(name);

        var existingItem = self.getFromStore(name, id);

        if (existingItem !== null) {
          existingItem.isLoading = true;
        }

        var promise = adapter.findOne(name, id).then(function(data) {
          return self.pushToStore(new Model(name, data));
        });

        if (existingItem !== null) {
          promise = promise.finally(function() {
            existingItem.isLoading = false;
          });
        }

        return promise;
      };

      Store.prototype.findMany = function(name, params) {
        var self = this;
        var Model = self.getModel(name);

        params = params || {};

        return adapter.findMany(name, params).then(function(data) {
          var items = [];

          for (var i = 0; i < data.length; i++) {
            var item = self.pushToStore(new Model(name, data[i]));
            items.push(item);
          }

          return items;
        });
      };

      Store.prototype.save = function(item) {
        var self = this;
        var id = item.getId();
        var name = item.name;
        var data = item.getData();
        var Model = self.getModel(name);
        var promise;
        var create = id === null;

        item.isSaving = true;

        if (create) {
          promise = adapter.create(name, data);
        } else {
          var existingItem = self.getFromStore(name, id);
          var copy = existingItem !== null && existingItem !== item;

          if (copy) {
            existingItem.isSaving = true;
          }

          promise = adapter.update(name, id, data);

          if (copy) {
            promise = promise.finally(function() {
              existingItem.isSaving = false;
            });
          }
        }

        promise = promise.then(function(data) {
          item.isValid = true;
          item.isError = false;
          item.errors = {};
          var savedItem = new Model(name, data).getData();
          item.update(savedItem);
          return self.pushToStore(item);
        });

        promise = promise.catch(function(data) {
          if (data.status === 422) {
            item.isValid = false;
            item.errors = data.errors;
          } else {
            item.isError = true;
          }

          return $q.reject(data);
        });

        promise = promise.finally(function() {
          item.isSaving = false;
        });

        return promise;
      };

      Store.prototype.remove = function(obj) {
        var id = obj.getId();
        var name = obj.name;

        obj.isSaving = true;
        obj.isDeleted = true;

        return adapter.remove(name, id)
          .catch(function() {
            obj.isDeleted = false;
          })
          .finally(function() {
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

      Store.prototype.addModelEventListener = function(name, event, callback) {
        if (this.modelEventListeners[name] === undefined) {
          this.modelEventListeners[name] = {};
        }

        if (this.modelEventListeners[name][event] === undefined) {
          this.modelEventListeners[name][event] = [];
        }

        this.modelEventListeners[name][event].push(callback);
      };

      Store.prototype.getModelEventListeners = function(name, event, callback) {
        if (this.modelEventListeners[name] === undefined) {
          return [];
        }

        return this.modelEventListeners[name][event] || [];
      };

      Store.prototype.getListeners = function(name, event) {
        var listeners = this.getEventListeners(event);
        return listeners.concat(this.getModelEventListeners(name, event));
      };

      Store.prototype.broadcast = function(name, event) {
        var args = Array.prototype.slice.call(1, arguments);
        var listeners = this.getListeners(name, event);

        _.forEach(listeners, function(listener) {
          listener(args);
        });
      };

      Store.prototype.on = function(name, event, callback) {
        if (callback === undefined) {
          callback = event;
          event = name;
          name = null;
        }

        if (name === null) {
          this.addEventListener(event, callback);
        } else {
          this.addModelEventListener(name, event, callback);
        }
      };

      return new Store(config);
    };
  });
})();
