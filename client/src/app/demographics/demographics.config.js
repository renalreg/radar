(function() {
  'use strict';

  var app = angular.module('radar.dialysis');

  app.config(function($stateProvider) {
    $stateProvider.state('patient.demographics', {
      url: '',
      templateUrl: 'app/demographics/demographics-list.html'
    });
  });
})();
