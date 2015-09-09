(function() {
  'use strict';

  var app = angular.module('radar.patients.renalImaging');

  app.config(function($stateProvider) {
    $stateProvider.state('patient.renalImaging', {
      url: '/renal-imaging',
      templateUrl: 'app/patients/renal-imaging/renal-imaging.html'
    });
  });

  app.constant('kidneyTypes', ['Natural', 'Transplant']);
  app.constant('imagingTypes', ['USS', 'CT', 'MRI']);
})();
