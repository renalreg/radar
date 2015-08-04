(function() {
  'use strict';

  var app = angular.module('radar.diseaseGroups');

  app.config(function($stateProvider) {
    $stateProvider.state('users', {
      url: '/users',
      templateUrl: 'app/users/user-list.html',
      controller: 'UserListController'
    });
  });
})();

