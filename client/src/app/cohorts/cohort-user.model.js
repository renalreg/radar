(function() {
  'use strict';

  var app = angular.module('radar.cohorts');

  app.factory('CohortUserModel', ['Model', '_', function(Model, _) {
    function CohortUserModel(modelName, data) {
      Model.call(this, modelName, data);
    }

    CohortUserModel.prototype = Object.create(Model.prototype);

    CohortUserModel.prototype.hasPermission = function(permission) {
      return _.indexOf(this.permissions, permission) >= 0;
    };

    return CohortUserModel;
  }]);

  app.config(['storeProvider', function(storeProvider) {
    storeProvider.registerModel('cohort-users', 'CohortUserModel');
  }]);
})();
