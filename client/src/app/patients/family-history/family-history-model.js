(function() {
  'use strict';

  var app = angular.module('radar.patients.familyHistory');

  app.factory('FamilyHistoryModel', ['Model', function(Model) {
    function FamilyHistoryModel(modelName, data) {
      if (data.relatives === undefined) {
        data.relatives = [];
      }

      Model.call(this, modelName, data);
    }

    FamilyHistoryModel.prototype = Object.create(Model.prototype);

    return FamilyHistoryModel;
  }]);

  app.config(['storeProvider', function(storeProvider) {
    storeProvider.registerModel('family-history', 'FamilyHistoryModel');
  }]);
})();
