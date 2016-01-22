(function() {
  'use strict';

  var app = angular.module('radar.patients.fetalUltrasounds');

  app.config(['storeProvider', function(storeProvider) {
    storeProvider.registerMixin('fetal-ultrasounds', 'SourceModelMixin');
  }]);
})();
