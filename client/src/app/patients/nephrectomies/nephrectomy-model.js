(function() {
  'use strict';

  var app = angular.module('radar.patients.nephrectomies');

  app.config(['storeProvider', function(storeProvider) {
    storeProvider.registerMixin('nephrectomies', 'SourceModelMixin');
  }]);
})();
