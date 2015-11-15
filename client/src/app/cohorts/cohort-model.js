(function() {
  'use strict';

  var app = angular.module('radar.cohorts');

  app.factory('CohortModel', ['Model', '$sce', function(Model, $sce) {
    function CohortModel(modelName, data) {
      Model.call(this, modelName, data);
    }

    CohortModel.prototype = Object.create(Model.prototype);

    CohortModel.prototype.getNotesHtml = function() {
      var notes = this.notes || '';
      return $sce.trustAsHtml(notes);
    };

    return CohortModel;
  }]);

  app.config(['storeProvider', function(storeProvider) {
    storeProvider.registerModel('cohorts', 'CohortModel');
  }]);
})();
