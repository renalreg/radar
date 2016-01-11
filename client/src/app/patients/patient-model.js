(function() {
  'use strict';

  var app = angular.module('radar.patients');

  app.factory('PatientModel', ['Model', 'store', '_', function(Model, store, _) {
    function PatientModel(modelName, data) {
      var i;

      if (data.groups !== undefined) {
        var groups = [];

        for (i = 0; i < data.groups.length; i++) {
          var rawGroup = data.groups[i];
          groups.push(store.pushToStore(new Model('group-patients', rawGroup)));
        }

        data.groups = groups;
      }

      Model.call(this, modelName, data);
    }

    PatientModel.prototype = Object.create(Model.prototype);

    PatientModel.prototype.getName = function() {
      if (this.firstName && this.lastName) {
        return this.firstName + ' ' + this.lastName;
      } else if (this.getId() !== null) {
        return 'Patient #' + this.getId();
      } else {
        return 'New Patient';
      }
    };

    PatientModel.prototype.getHospitals = function() {
      return _.filter(this.groups, function(x) {
        return x.group.type === 'HOSPITAL';
      });
    };

    PatientModel.prototype.getCohorts = function(all) {
      return _.filter(this.groups, function(x) {
        return x.group.type === 'COHORT';
      });
    };

    return PatientModel;
  }]);

  app.config(['storeProvider', function(storeProvider) {
    storeProvider.registerModel('patients', 'PatientModel');
  }]);
})();
