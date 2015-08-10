(function() {
  'use strict';

  var app = angular.module('radar.renalImaging');

  app.config(function($stateProvider) {
    $stateProvider.state('patient.renalImaging', {
      url: '/renal-imaging',
      templateUrl: 'app/renal-imaging/renal-imaging.html',
      controller: 'RenalImagingController'
    });
  });
})();

