(function() {
  'use strict';

  var app = angular.module('radar.patients.renalImaging');

  app.config(['$stateProvider', function($stateProvider) {
    $stateProvider.state('patient.renalImaging', {
      url: '/renal-imaging',
      templateUrl: 'app/patients/renal-imaging/renal-imaging.html'
    });
  }]);
})();
