(function() {
  'use strict';

  var app = angular.module('radar.patients');

  app.factory('PatientModel', ['Model', 'store', '_', function(Model, store, _) {
    function PatientModel(modelName, data) {
      var i;

      if (data.cohorts !== undefined) {
        var cohorts = [];

        for (i = 0; i < data.cohorts.length; i++) {
          var rawCohort = data.cohorts[i];
          cohorts.push(store.pushToStore(new Model('cohort-patients', rawCohort)));
        }

        data.cohorts = cohorts;
      }

      if (data.organisations !== undefined) {
        var organisations = [];

        for (i = 0; i < data.organisations.length; i++) {
          var rawOrganisation = data.organisations[i];
          organisations.push(store.pushToStore(new Model('organisation-patients', rawOrganisation)));
        }

        data.organisations = organisations;
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

    PatientModel.prototype.getUnits = function() {
      return _.filter(this.organisations, function(x) {
        return x.organisation.type === 'UNIT';
      });
    };

    return PatientModel;
  }]);

  app.config(['storeProvider', function(storeProvider) {
    storeProvider.registerModel('patients', 'PatientModel');
  }]);
})();

