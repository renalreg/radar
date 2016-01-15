(function() {
  'use strict';

  var app = angular.module('radar.patients.medications');

  app.factory('MedicationModel', ['Model', 'lazyLoad', function(Model, lazyLoad) {
    function MedicationModel(modelName, data) {
      Model.call(this, modelName, data);
    }

    MedicationModel.prototype = Object.create(Model.prototype);

    MedicationModel.prototype.getDrug = function() {
      var r;

      if (this.drug) {
        r = this.drug.name;
      } else {
        r = this.drugText;
      }

      return r;
    };

    MedicationModel.prototype.getDose = function() {
      var r;

      if (this.doseQuantity !== undefined && this.doseQuantity !== null) {
        r = this.doseQuantity;

        if (this.doseUnit) {
          r = r + ' ' + this.doseUnit.label;
        }
      } else {
        r = this.doseText;
      }

      return r;
    };

    return MedicationModel;
  }]);

  app.config(['storeProvider', function(storeProvider) {
    storeProvider.registerModel('medications', 'MedicationModel');
    storeProvider.registerMixin('medications', 'SourceModelMixin');
  }]);
})();
