(function() {
  'use strict';

  var app = angular.module('radar.users');

  app.factory('UserModel', ['Model', 'store', '_', function(Model, store, _) {
    function filterGroupUsersByType(groupUsers, groupType) {
      return _.filter(groupUsers, function(x) {
        return x.group.type === groupType;
      });
    }

    function uniqueGroups(groupUsers) {
      var groups = _.map(groupUsers, function(x) {
        return x.group;
      });

      groups = _.uniqBy(groups, 'id');

      return groups;
    }

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

    UserModel.prototype.getCohortUsers = function() {
      return filterGroupUsersByType(this.groups, 'COHORT');
    };

    UserModel.prototype.getHospitalUsers = function() {
      return filterGroupUsersByType(this.groups, 'HOSPITAL');
    };

    UserModel.prototype.getCohorts = function() {
      var groupUsers = this.getCohortUsers();
      var groups = uniqueGroups(groupUsers);
      return groups;
    };

    UserModel.prototype.getHospitals = function() {
      var groupUsers = this.getHospitalUsers();
      var groups = uniqueGroups(groupUsers);
      return groups;
    };

    return UserModel;
  }]);

  app.config(['storeProvider', function(storeProvider) {
    storeProvider.registerModel('users', 'UserModel');
  }]);
})();
