(function() {
  'use strict';

  var app = angular.module('radar.patients.results');

  app.factory('ResultGroupModel', function(Model, store) {
    function ResultGroupModel(modelName, data) {
      if (data.resultGroupSpec !== undefined) {
        // Save space by only keeping one copy
        var ResultGroupSpecModel = store.getModelConstructor('result-group-specs');
        data.resultGroupSpec = store.pushToStore(new ResultGroupSpecModel('result-group-specs', data.resultGroupSpec));
      }

      Model.call(this, modelName, data);
    }

    ResultGroupModel.prototype = Object.create(Model.prototype);

    ResultGroupModel.prototype.getValue = function(code) {
      var value = this.results[code];

      if (value === undefined || value === null) {
        return null;
      } else {
        if (angular.isObject(value)) {
          return value.label;
        } else {
          return value;
        }
      }
    };

    return ResultGroupModel;
  });

  app.config(function(storeProvider) {
    storeProvider.registerModel('result-groups', 'ResultGroupModel');
  });
})();
