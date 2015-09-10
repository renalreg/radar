(function() {
  'use strict';

  var app = angular.module('radar.patients.demographics');

  app.factory('PatientAddressModel', function(Model) {
    function PatientAddressModel(modelName, data) {
      Model.call(this, modelName, data);
    }

    PatientAddressModel.prototype = Object.create(Model.prototype);

    PatientAddressModel.prototype.address = function() {
      var lines = [];

      if (this.addressLine1) {
        lines.push(this.addressLine1);
      }

      if (this.addressLine2) {
        lines.push(this.addressLine2);
      }

      if (this.addressLine3) {
        lines.push(this.addressLine3);
      }

      if (this.postcode) {
        lines.push(this.postcode);
      }

      return lines.join('\n');
    };

    return PatientAddressModel;
  });

  app.config(function(storeProvider) {
    storeProvider.registerModel('patient-addresses', 'PatientAddressModel');
  });
})();


