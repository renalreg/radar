(function() {
  'use strict';

  var app = angular.module('radar.auth');

  app.controller('LoginController', function($scope, session, loginService, $state) {
    $scope.username = '';
    $scope.password = '';

    $scope.login = function() {
      loginService.login($scope.username, $scope.password).then(function() {
        $state.go('patients');
      });
    };

    $scope.logout = function() {
      session.logout();
    };
  });
})();
