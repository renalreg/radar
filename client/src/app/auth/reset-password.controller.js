(function() {
  'use strict';

  var app = angular.module('radar');

  app.controller('ResetPasswordController', ['$scope', '$state', 'authService', '$stateParams', function($scope, $state, authService, $stateParams) {
    $scope.errors = {};
    $scope.data = {};

    var token = $stateParams.token;

    $scope.submit = function() {
      $scope.errors = {};

      authService.resetPassword(token, $scope.data.username, $scope.data.password)
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
