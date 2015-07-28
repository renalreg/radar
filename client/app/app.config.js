(function() {
  'use strict';

  var app = angular.module('radar');

  app.config(function($routeProvider) {
    $routeProvider.when('/patients', {
      templateUrl: 'patient-list.html',
      controller: 'PatientListController'
    });

    $routeProvider.otherwise({redirectTo: '/patients'});
  });
})();
