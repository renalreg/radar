(function() {
  'use strict';

  var app = angular.module('radar.patients.hospitalisations');

  app.config(['storeProvider', function(storeProvider) {
    storeProvider.registerMixin('hospitalisations', 'SourceModelMixin');
  }]);
})();
