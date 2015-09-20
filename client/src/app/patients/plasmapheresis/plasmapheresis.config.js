(function() {
  'use strict';

  var app = angular.module('radar.patients.plasmapheresis');

  app.config(['$stateProvider', function($stateProvider) {
    $stateProvider.state('patient.plasmapheresis', {
      url: '/plasmapheresis',
      templateUrl: 'app/patients/plasmapheresis/plasmapheresis.html'
    });
  }]);
})();
