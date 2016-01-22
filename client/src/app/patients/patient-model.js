(function() {
  'use strict';

  var app = angular.module('radar.patients');

  app.factory('PatientModel', ['Model', 'store', '_', function(Model, store, _) {
    function filterGroupPatientsByType(groupPatients, groupType) {
      return _.filter(groupPatients, function(x) {
        return x.group.type === groupType;
      });
    }

    function filterGroupPatientsByCurrent(groupPatients) {
      return _.filter(groupPatients, function(x) {
        return x.current;
      });
    }

    function uniqueGroups(groupPatients) {
      var groups = _.map(groupPatients, function(x) {
        return x.group;
      });

      groups = _.uniqBy(groups, 'id');

      return groups;
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

    PatientModel.prototype.getHospitalPatients = function() {
      return filterGroupPatientsByType(this.groups, 'HOSPITAL');
    };

    PatientModel.prototype.getCohortPatients = function(all) {
      return filterGroupPatientsByType(this.groups, 'COHORT');
    };

    PatientModel.prototype.getCurrentHospitalPatients = function() {
      return filterGroupPatientsByCurrent(this.getHospitalPatients());
    };

    PatientModel.prototype.getCurrentCohortPatients = function() {
      return filterGroupPatientsByCurrent(this.getCohortPatients());
    };

    PatientModel.prototype.getCohorts = function(all) {
      return uniqueGroups(this.getCohortPatients());
    };

    PatientModel.prototype.getHospitals = function(all) {
      return uniqueGroups(this.getHospitalPatients());
    };

    PatientModel.prototype.getCurrentCohorts = function(all) {
      return uniqueGroups(this.getCurrentCohortPatients());
    };

    PatientModel.prototype.getCurrentHospitals = function(all) {
      return uniqueGroups(this.getCurrentHospitalPatients());
    };

    return PatientModel;
  }]);

  app.config(['storeProvider', function(storeProvider) {
    storeProvider.registerModel('patients', 'PatientModel');
  }]);
})();
