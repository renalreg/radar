(function() {
  'use strict';

  var app = angular.module('radar');

  var MESSAGE = 'Check your email for a link to reset your password.';

  app.controller('ForgotPasswordController', ['$scope', '$state', 'authService', 'notificationService', function($scope, $state, authService, notificationService) {
    $scope.errors = {};
    $scope.data = {};

    $scope.submit = function() {
      $scope.errors = {};

      authService.forgotPassword($scope.data.username)
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
  }]);
})();
