(function() {
  'use strict';

  var app = angular.module('radar.patients');

  app.factory('PatientModel', function(Model, store, _) {
    function PatientModel(modelName, data) {
      Model.call(this, modelName, data);

      var i;
      var cohorts = [];
      var organisations = [];

      for (i = 0; i < this.cohorts.length; i++) {
        var rawCohort = this.cohorts[i];
        cohorts.push(store.pushToStore(new Model('patient-cohorts', rawCohort)));
      }

      for (i = 0; i < this.organisations.length; i++) {
        var rawOrganisation = this.organisations[i];
        organisations.push(store.pushToStore(new Model('patient-organisations', rawOrganisation)));
      }

      this.cohorts = cohorts;
      this.organisations = organisations;
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
  });

  app.config(function(storeProvider) {
    storeProvider.registerModel('patients', 'PatientModel');
  });
})();

