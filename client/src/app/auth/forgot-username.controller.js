(function() {
  'use strict';

  var app = angular.module('radar');

  var MESSAGE = 'Check your email for a reminder of your username(s).';

  function ForgotUsernameController(
    $scope, $state, authService, notificationService
  ) {
    $scope.errors = {};
    $scope.data = {};

    $scope.submit = function() {
      $scope.errors = {};

      return authService.forgotUsername($scope.data.email)
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

  ForgotUsernameController.$inject = [
    '$scope', '$state', 'authService', 'notificationService'
  ];

  app.controller('ForgotUsernameController', ForgotUsernameController);
})();
