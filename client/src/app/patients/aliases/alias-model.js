(function() {
  'use strict';

  var app = angular.module('radar.patients.aliases');

  app.config(['storeProvider', function(storeProvider) {
    storeProvider.registerMixin('patient-aliases', 'SourceModelMixin');
  }]);
})();
