(function() {
  'use strict';

  var app = angular.module('radar.auth');

  app.controller('LoginController', function($scope, session, loginService, $state) {
    var credentials = {
      username: '',
      password: ''
    };
    $scope.credentials = credentials;

    $scope.errors = {};

    $scope.login = function() {
      $scope.errors = {};

      loginService.login(credentials.username, credentials.password)
        .then(function() {
          $state.go('patients');
        })
        .catch(function(errors) {
          if (errors) {
            $scope.errors = errors;
          }
        });
    };

    $scope.logout = function() {
      session.logout();
    };
  });
})();
