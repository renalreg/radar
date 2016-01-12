(function() {
  'use strict';

  var app = angular.module('radar.patients.comorbidities');

  app.config(['storeProvider', function(storeProvider) {
    storeProvider.registerMixin('comorbidities', 'SourceModelMixin');
  }]);
})();
