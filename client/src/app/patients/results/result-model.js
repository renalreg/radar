(function() {
  'use strict';

  var app = angular.module('radar.patients.results');

  app.factory('ResultModel', ['Model', 'store', function(Model, store) {
    function ResultModel(modelName, data) {
      if (data.observation) {
        // Save space by only keeping one copy
        var ObservationModel = store.getModelConstructor('observations');
        data.observation = store.pushToStore(new ObservationModel('observations', data.observation));
      }

      Model.call(this, modelName, data);
    }

    ResultModel.prototype = Object.create(Model.prototype);

    ResultModel.prototype.getDisplayValue = function() {
      return this.value.description || this.value;
    };

    return ResultModel;
  }]);

  app.config(['storeProvider', function(storeProvider) {
    storeProvider.registerModel('results', 'ResultModel');
    storeProvider.registerMixin('results', 'SourceModelMixin');
  }]);
})();
