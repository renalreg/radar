(function() {
  'use strict';

  var app = angular.module('radar.patients.results');

  app.factory('ResultGroupSpecModel', function(Model, store) {
    function ResultGroupSpecModel(modelName, data) {
      if (data.resultSpecs !== undefined) {
        var resultSpecs = [];

        for (var i = 0; i < data.resultSpecs.length; i++) {
          var resultSpec = data.resultSpecs[i];
          var ResultSpecModel = store.getModelConstructor('result-specs');
          resultSpecs.push(store.pushToStore(new ResultSpecModel('result-specs', resultSpec)));
        }

        data.resultSpecs = resultSpecs;
      }

      Model.call(this, modelName, data);
    }

    ResultGroupSpecModel.prototype = Object.create(Model.prototype);

    return ResultGroupSpecModel;
  });

  app.config(function(storeProvider) {
    storeProvider.registerModel('result-group-specs', 'ResultGroupSpecModel');
  });
})();
