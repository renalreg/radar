(function() {
  'use strict';

  var app = angular.module('radar.patients.plasmapheresis');

  app.config(['storeProvider', function(storeProvider) {
    storeProvider.registerMixin('plasmapheresis', 'SourceModelMixin');
  }]);
})();
