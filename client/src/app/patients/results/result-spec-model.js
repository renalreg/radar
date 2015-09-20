(function() {
  'use strict';

  var app = angular.module('radar.patients.results');

  app.factory('ResultSpecModel', ['Model', function(Model) {
    function ResultSpecModel(modelName, data) {
      Model.call(this, modelName, data);
    }

    ResultSpecModel.prototype = Object.create(Model.prototype);

    return ResultSpecModel;
  }]);

  app.config(['storeProvider', function(storeProvider) {
    storeProvider.registerModel('result-specs', 'ResultSpecModel');
  }]);
})();
