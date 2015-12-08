(function() {
  'use strict';

  var app = angular.module('radar');

  var MESSAGE = 'Check your email for a link to reset your password.';

  function ForgotPasswordController(
    $scope, $state, authService, notificationService
  ) {
    $scope.errors = {};
    $scope.data = {};

    $scope.submit = function() {
      $scope.errors = {};

      return authService.forgotPassword($scope.data.username, $scope.data.email)
        .then(function() {
          notificationService.success({message: MESSAGE, timeout: 30000});
          $state.go('login');
        })
        ['catch'](function(errors) {
          if (errors) {
            $scope.errors = errors;
          }
        });
    };
  }

  ForgotPasswordController.$inject = [
    '$scope', '$state', 'authService', 'notificationService'
  ];

  app.controller('ForgotPasswordController', ForgotPasswordController);
})();
