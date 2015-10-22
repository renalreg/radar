(function() {
  'use strict';

  var app = angular.module('radar');

  app.controller('ForgotUsernameController', ['$scope', '$state', 'authService', function($scope, $state, authService) {
    $scope.errors = {};
    $scope.data = {};

    $scope.submit = function() {
      $scope.errors = {};

      authService.forgotUsername($scope.data.email)
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
