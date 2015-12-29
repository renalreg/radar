(function() {
  'use strict';

  var app = angular.module('radar.patients.addresses');

  app.factory('PatientAddressModel', ['Model', function(Model) {
    function PatientAddressModel(modelName, data) {
      Model.call(this, modelName, data);
    }

    PatientAddressModel.prototype = Object.create(Model.prototype);

    PatientAddressModel.prototype.getAddress = function() {
      var lines = [];

      if (this.address1) {
        lines.push(this.address1);
      }

      if (this.address2) {
        lines.push(this.address2);
      }

      if (this.address3) {
        lines.push(this.address3);
      }

      if (this.postcode) {
        lines.push(this.postcode);
      }

      return lines.join(',\n');
    };

    return PatientAddressModel;
  }]);

  app.config(['storeProvider', function(storeProvider) {
    storeProvider.registerModel('patient-addresses', 'PatientAddressModel');
  }]);
})();
