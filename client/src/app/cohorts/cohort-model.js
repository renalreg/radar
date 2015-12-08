(function() {
  'use strict';

  var app = angular.module('radar.cohorts');

  app.factory('CohortModel', ['Model', 'safeHtml', function(Model, safeHtml) {
    function CohortModel(modelName, data) {
      // Mark the notes HTML as safe
      data.notes = safeHtml(data.notes);

      Model.call(this, modelName, data);
    }

    CohortModel.prototype = Object.create(Model.prototype);

    return CohortModel;
  }]);

  app.config(['storeProvider', function(storeProvider) {
    storeProvider.registerModel('cohorts', 'CohortModel');
  }]);
})();
