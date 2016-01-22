(function() {
  'use strict';

  var app = angular.module('radar.patients.renalImaging');

  app.config(['storeProvider', function(storeProvider) {
    storeProvider.registerMixin('renal-imaging', 'SourceModelMixin');
  }]);
})();
