(function() {
  'use strict';

  var app = angular.module('radar');

  app.config(function(RestangularProvider) {
    RestangularProvider.setBaseUrl('http://localhost:5000');
    RestangularProvider.setRequestSuffix('/');

    RestangularProvider.addResponseInterceptor(function(data, operation) {
      if (operation === 'getList') {
        return data.data;
      } else {
        return data;
      }
    });
  });

  app.config(function($routeProvider) {
    $routeProvider.when('/patients', {
      templateUrl: 'app/patient-list.html',
      controller: 'PatientListController'
    });

    $routeProvider.otherwise({redirectTo: '/patients'});
  });
})();
