(function() {
  'use strict';

  var app = angular.module('radar.patients.demographics');

  app.config(['storeProvider', function(storeProvider) {
    storeProvider.registerMixin('patient-demographics', 'SourceModelMixin');
  }]);
})();
