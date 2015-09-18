(function() {
  'use strict';

  var app = angular.module('radar.users');

  app.factory('UserModel', function(Model, store, _) {
    function UserModel(modelName, data) {
      Model.call(this, modelName, data);

      var i;
      var cohorts = [];
      var organisations = [];

      for (i = 0; i < this.cohorts.length; i++) {
        var rawCohort = this.cohorts[i];
        cohorts.push(store.pushToStore(new Model('cohort-users', rawCohort)));
      }

      for (i = 0; i < this.organisations.length; i++) {
        var rawOrganisation = this.organisations[i];
        organisations.push(store.pushToStore(new Model('organisation-users', rawOrganisation)));
      }

      this.cohorts = cohorts;
      this.organisations = organisations;
    }

    UserModel.prototype = Object.create(Model.prototype);

    UserModel.prototype.getUnits = function() {
      return _.filter(this.organisations, function(x) {
        return x.organisation.type === 'UNIT';
      });
    };

    return UserModel;
  });

  app.config(function(storeProvider) {
    storeProvider.registerModel('users', 'UserModel');
  });
})();


