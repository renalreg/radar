(function() {
  'use strict';

  var app = angular.module('radar.users');

  app.factory('UserModel', ['Model', 'store', '_', function(Model, store, _) {
    function UserModel(modelName, data) {
      var i;

      if (data === undefined) {
        data = {};
      }

      if (data.groups === undefined) {
        data.groups = [];
      } else {
        var groups = [];

        for (i = 0; i < data.groups.length; i++) {
          var rawGroup = data.groups[i];
          groups.push(store.pushToStore(store.create('group-users', rawGroup)));
        }

        data.groups = groups;
      }

      Model.call(this, modelName, data);
    }

    UserModel.prototype = Object.create(Model.prototype);

    UserModel.prototype.getCohorts = function() {
      return _.filter(this.groups, function(x) {
        return x.group.type === 'COHORT';
      });
    };

    UserModel.prototype.getHospitals = function() {
      return _.filter(this.groups, function(x) {
        return x.group.type === 'HOSPITAL';
      });
    };

    return UserModel;
  }]);

  app.config(['storeProvider', function(storeProvider) {
    storeProvider.registerModel('users', 'UserModel');
  }]);
})();
