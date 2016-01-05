(function() {
  'use strict';

  var app = angular.module('radar.patients.transplants');

  app.factory('TransplantModel', ['Model', function(Model) {
    function TransplantModel(modelName, data) {
      if (data.biopsies === undefined) {
        data.biopsies = [];
      }

      if (data.rejections === undefined) {
        data.rejections = [];
      }

      Model.call(this, modelName, data);
    }

    TransplantModel.prototype = Object.create(Model.prototype);

    return TransplantModel;
  }]);

  app.config(['storeProvider', function(storeProvider) {
    storeProvider.registerModel('transplants', 'TransplantModel');
  }]);
})();
