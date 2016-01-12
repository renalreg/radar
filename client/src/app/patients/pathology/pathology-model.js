(function() {
  'use strict';

  var app = angular.module('radar.patients.pathology');

  app.config(['storeProvider', function(storeProvider) {
    storeProvider.registerMixin('pathology', 'SourceModelMixin');
  }]);
})();
