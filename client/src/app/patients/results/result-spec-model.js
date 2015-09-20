(function() {
  'use strict';

  var app = angular.module('radar.patients.results');

  app.factory('ResultSpecModel', function(Model, _) {
    function ResultSpecModel(modelName, data) {
      if (data.code !== undefined) {
        data.code = _.camelCase(data.code);
      }

      if (data.type !== undefined) {
        data.type = _.camelCase(data.type);
      }

      Model.call(this, modelName, data);
    }

    ResultSpecModel.prototype = Object.create(Model.prototype);

    return ResultSpecModel;
  });

  app.config(function(storeProvider) {
    storeProvider.registerModel('result-specs', 'ResultSpecModel');
  });
})();
