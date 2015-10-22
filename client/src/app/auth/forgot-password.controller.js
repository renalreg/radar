(function() {
  'use strict';

  var app = angular.module('radar');

  app.controller('ForgotPasswordController', ['$scope', '$state', 'authService', function($scope, $state, authService) {
    $scope.errors = {};
    $scope.data = {};

    $scope.submit = function() {
      $scope.errors = {};

      authService.forgotPassword($scope.data.username)
        .then(function() {
          // TODO show message
          $state.go('login');
        })
        ['catch'](function(errors) {
          if (errors) {
            $scope.errors = errors;
          }
        });
    };
  }]);
})();
