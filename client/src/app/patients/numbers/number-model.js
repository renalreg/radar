(function() {
  'use strict';

  var app = angular.module('radar.patients.numbers');

  app.config(['storeProvider', function(storeProvider) {
    storeProvider.registerMixin('patient-numbers', 'SourceModelMixin');
  }]);
})();
