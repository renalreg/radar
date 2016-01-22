(function() {
  'use strict';

  var app = angular.module('radar.patients.fetalAnomalyScans');

  app.config(['storeProvider', function(storeProvider) {
    storeProvider.registerMixin('fetal-anomaly-scans', 'SourceModelMixin');
  }]);
})();
