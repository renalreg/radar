(function() {
  'use strict';

  var app = angular.module('radar.logs');

  app.factory('LogModel', ['Model', '_', function(Model, _) {
    function LogModel(modelName, data) {
      Model.call(this, modelName, data);
    }

    LogModel.prototype = Object.create(Model.prototype);

    LogModel.prototype.hasChanges = function() {
      return this.type === 'INSERT' || this.type === 'UPDATE' || this.type === 'DELETE';
    };

    LogModel.prototype.getChanges = function() {
      if (this._changes === undefined) {
        var changes = null;

        var originalData = this.originalData || {};
        var newData = this.newData || {};

        if (this.type === 'INSERT') {
          changes = _.map(newData || {}, function(newValue, column) {
            return {
              column: column,
              newValue: newValue
            };
          });
        } else if (this.type === 'DELETE') {
          changes = _.map(originalData || {}, function(originalValue, column) {
            return {
              column: column,
              originalValue: originalValue
            };
          });
        } else if (this.type === 'UPDATE') {
          changes = [];

          _.forEach(newData, function(newValue, column) {
            var originalValue = originalData[column];

            if (originalValue !== newValue) {
              changes.push({
                column: column,
                originalValue: originalValue,
                newValue: newValue
              });
            }
          });
        }

        this._changes = changes;
      }

      return this._changes;
    };

    return LogModel;
  }]);

  app.config(['storeProvider', function(storeProvider) {
    storeProvider.registerModel('logs', 'LogModel');
  }]);
})();
