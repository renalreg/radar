(function() {
  'use strict';

  var app = angular.module('radar.users.new');

  app.config(['$stateProvider', function($stateProvider) {
    $stateProvider.state('newUser', {
      url: '/users/new',
      templateUrl: 'app/users/new/new-user.html'
    });
  }]);
})();
