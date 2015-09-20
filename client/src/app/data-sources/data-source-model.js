(function() {
  'use strict';

  var app = angular.module('radar.patients');

  app.factory('DataSourceModel', ['Model', function(Model) {
    function DataSourceModel(modelName, data) {
      Model.call(this, modelName, data);
    }

    DataSourceModel.prototype = Object.create(Model.prototype);

    DataSourceModel.prototype.getName = function() {
      var self = this;

      if (self.type === 'RADAR') {
        return self.organisation.name;
      } else {
        return self.organisation.name + ' (' + self.type + ')';
      }
    };

    return DataSourceModel;
  }]);

  app.config(['storeProvider', function(storeProvider) {
    storeProvider.registerModel('data-sources', 'DataSourceModel');
    storeProvider.registerChildModel('dataSource', 'data-sources');
    storeProvider.registerChildModel('dataSources', 'data-sources');
  }]);
})();
