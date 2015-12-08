(function() {
  'use strict';

  var app = angular.module('radar.cohorts');

  app.factory('OrganisationUserModel', ['Model', '_', function(Model, _) {
    function OrganisationUserModel(modelName, data) {
      Model.call(this, modelName, data);
    }

    OrganisationUserModel.prototype = Object.create(Model.prototype);

    OrganisationUserModel.prototype.hasPermission = function(permission) {
      return _.indexOf(this.permissions, permission) >= 0;
    };

    return OrganisationUserModel;
  }]);

  app.config(['storeProvider', function(storeProvider) {
    storeProvider.registerModel('organisation-users', 'OrganisationUserModel');
  }]);
})();
