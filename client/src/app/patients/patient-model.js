(function() {
  'use strict';

  var app = angular.module('radar.patients');

  app.factory('PatientModel', ['Model', 'store', '_', function(Model, store, _) {
    function filterByCurrent(groups) {
      return _.filter(groups, function(x) {
        return x.current;
      });
    }

    function filterByType(groups, type) {
      return _.filter(groups, function(x) {
        return x.group.type === type;
      });
    }

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
      return filterByType(this.groups, 'HOSPITAL');
    };

    PatientModel.prototype.getCurrentHospitals = function(all) {
      return filterByCurrent(this.getHospitals());
    };

    PatientModel.prototype.getCohorts = function(all) {
      return filterByType(this.groups, 'COHORT');
    };

    PatientModel.prototype.getCurrentCohorts = function(all) {
      return filterByCurrent(this.getCohorts());
    };

    return PatientModel;
  }]);

  app.config(['storeProvider', function(storeProvider) {
    storeProvider.registerModel('patients', 'PatientModel');
  }]);
})();
