(function() {
  'use strict';

  var app = angular.module('radar.store');

  app.factory('Model', function(_, store, md5, flattenRelationships) {
    function _hash(data) {
      var keys = _.sortBy(_.keys(data));
      var values = [];

      _.forEach(keys, function(key) {
        var value = data[key];

        if (angular.isArray(value)) {
          _.forEach(value, function(x) {
            values = values.concat(_hash(x));
          })
        } else if (angular.isObject(value)) {
          values = values.concat(_hash(value));
        } else {
          values.push(value);
        }
      });

      return values;
    }

    function hash(data) {
      data = flattenRelationships(data);
      var values = _hash(data);
      return values.join('');
    }

    function Model(modelName, data) {
      var self = this;

      self.modelName = modelName;
      self.isSaving = false;
      self.isDeleted = false;
      self.isValid = true;
      self.isError = false;
      self.isLoading = false;
      self.errors = {};

      self.hash = "";

      self.meta = [];
      self.meta = _.keysIn(self);

      self.update(data);
    }

    Model.prototype.isDirty = function() {
      return this.hash != hash(this.getData());
    };

    Model.prototype.update = function(data) {
      var self = this;

      var keys = _.keys(self);
      keys = _.difference(keys, self.meta);

      for (var i = 0; i < keys.length; i++) {
        var key = keys[i];
        delete this[key];
      }

      self.hash = hash(data);

      _.forEach(data, function(value, key) {
        self[key] = value;
      });
    };

    Model.prototype.getData = function() {
      // TODO call getData on children too
      return _.omit(this, this.meta);
    };

    Model.prototype.getId = function() {
      return this.id || null;
    };

    Model.prototype.save = function() {
      return store.save(this);
    };

    Model.prototype.revert = function() {
      this.update(this.originalData);
    };

    Model.prototype.reload = function() {
      var id = this.getId();

      if (id !== null) {
        store.findOne(this.modelName, id);
      }
    };

    Model.prototype.remove = function() {
      return store.remove(this);
    };

    Model.prototype.clone = function() {
      var Model = store.getModelConstructor(this.modelName);
      return new Model(this.modelName, this.getData());
    };

    return Model;
  });
})();
