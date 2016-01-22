(function() {
  'use strict';

  var app = angular.module('radar.patients.dialysis');

  app.config(['storeProvider', function(storeProvider) {
    storeProvider.registerMixin('dialysis', 'SourceModelMixin');
  }]);
})();
