(function() {
  'use strict';

  var app = angular.module('radar');

  app.config(['adapterProvider', function(adapterProvider) {
    adapterProvider.setBaseUrl('http://localhost:5001');
  }]);
})();
