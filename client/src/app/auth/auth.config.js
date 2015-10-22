(function() {
  'use strict';

  var app = angular.module('radar.auth');

  app.config(['$stateProvider', function($stateProvider) {
    $stateProvider.state('login', {
      url: '/login',
      templateUrl: 'app/auth/login.html'
    });

    $stateProvider.state('forgotUsername', {
      url: '/forgot-username',
      controller: 'ForgotUsernameController',
      templateUrl: 'app/auth/forgot-username.html'
    });

    $stateProvider.state('forgotPassword', {
      url: '/forgot-password',
      controller: 'ForgotPasswordController',
      templateUrl: 'app/auth/forgot-password.html'
    });

    $stateProvider.state('resetPassword', {
      url: '/reset-password/:token',
      controller: 'ResetPasswordController',
      templateUrl: 'app/auth/reset-password.html'
    });
  }]);
})();
