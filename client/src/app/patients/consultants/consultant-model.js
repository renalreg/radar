(function() {
  'use strict';

  var app = angular.module('radar.patients.consultants');

  app.factory('PatientConsultantModel', ['Model', 'store', function(Model, store) {
    function PatientConsultantModel(modelName, data) {
      if (data.consultant) {
        data.consultant = store.create('consultants', data.consultant);
      }

      Model.call(this, modelName, data);
    }

    PatientConsultantModel.prototype = Object.create(Model.prototype);

    return PatientConsultantModel;
  }]);

  app.config(['storeProvider', function(storeProvider) {
    storeProvider.registerModel('patient-consultants', 'PatientConsultantModel');
  }]);
})();
