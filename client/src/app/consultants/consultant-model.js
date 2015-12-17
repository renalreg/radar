(function() {
  'use strict';

  var app = angular.module('radar.consultants');

  app.factory('ConsultantModel', ['Model', function(Model) {
    function ConsultantModel(modelName, data) {
      if (data.organisationConsultants === undefined) {
        data.organisationConsultants = [];
      }

      Model.call(this, modelName, data);
    }

    ConsultantModel.prototype = Object.create(Model.prototype);

    ConsultantModel.prototype.toString = function() {
      return this.title + ' ' + this.firstName + ' ' + this.lastName;
    };

    return ConsultantModel;
  }]);

  app.config(['storeProvider', function(storeProvider) {
    storeProvider.registerModel('consultants', 'ConsultantModel');
  }]);
})();
