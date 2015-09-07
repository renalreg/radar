(function() {
  'use strict';

  var app = angular.module('radar.account');

  app.config(function($stateProvider) {
    $stateProvider.state('account', {
      url: '/account',
      templateUrl: 'app/account/account.html'
    });

    $stateProvider.state('changePassword', {
      url: '/change-password',
      templateUrl: 'app/account/change-password.html'
    });

    $stateProvider.state('changeEmail', {
      url: '/change-email',
      templateUrl: 'app/account/change-email.html'
    });
  });
})();
