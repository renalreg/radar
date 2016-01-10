(function() {
  'use strict';

  var app = angular.module('radar.patients.results');

  app.factory('ResultModel', ['Model', 'store', function(Model, store) {
    function ResultModel(modelName, data) {
      if (data.observation !== undefined) {
        // Save space by only keeping one copy
        var ObservationModel = store.getModelConstructor('observations');
        data.observation = store.pushToStore(new ObservationModel('observations', data.observation));
      }

      Model.call(this, modelName, data);
    }

    ResultModel.prototype = Object.create(Model.prototype);

    return ResultModel;
  }]);

  app.config(['storeProvider', function(storeProvider) {
    storeProvider.registerModel('results', 'ResultModel');
  }]);
})();
