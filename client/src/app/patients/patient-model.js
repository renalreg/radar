(function() {
  'use strict';

  var app = angular.module('radar.patients');

  app.factory('PatientModel', function(Model, store) {
    function PatientModel(name, data) {
      Model.call(this, name, data);

      var i;
      var diseaseGroups = [];
      var units = [];

      for (i = 0; i < this.diseaseGroups.length; i++) {
        var rawDiseaseGroup = this.diseaseGroups[i];
        diseaseGroups.push(store.pushToStore(new Model('patient-disease-groups', rawDiseaseGroup)));
      }

      for (i = 0; i < this.units.length; i++) {
        var rawUnit = this.units[i];
        units.push(store.pushToStore(new Model('patient-units', rawUnit)));
      }

      this.diseaseGroups = diseaseGroups;
      this.units = units;
    }

    PatientModel.prototype = Object.create(Model.prototype);

    return PatientModel;
  });

  app.config(function(storeProvider) {
    storeProvider.registerModel('patients', 'PatientModel');
  });
})();

