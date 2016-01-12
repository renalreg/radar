(function() {
  'use strict';

  var app = angular.module('radar.patients.medications');

  app.config(['storeProvider', function(storeProvider) {
    storeProvider.registerMixin('medications', 'SourceModelMixin');
  }]);
})();
