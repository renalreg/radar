(function() {
  'use strict';

  var app = angular.module('radar.groups');

  app.factory('GroupUserModel', ['Model', '_', function(Model, _) {
    function GroupUserModel(modelName, data) {
      Model.call(this, modelName, data);
    }

    GroupUserModel.prototype = Object.create(Model.prototype);

    GroupUserModel.prototype.hasPermission = function(permission) {
      return _.indexOf(this.permissions, permission) >= 0;
    };

    return GroupUserModel;
  }]);

  app.config(['storeProvider', function(storeProvider) {
    storeProvider.registerModel('group-users', 'GroupUserModel');
  }]);
})();
