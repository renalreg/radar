(function() {
  'use strict';

  var app = angular.module('radar.admin');

  app.config(['$stateProvider', function($stateProvider) {
    $stateProvider.state('admin', {
      url: '/admin',
      templateUrl: 'app/admin/admin.html'
    });
  }]);
})();
