(function() {
  'use strict';

  var app = angular.module('radar.users');

  function DeleteUserController($scope, user, session, notificationService, $state) {
    $scope.user = user;
    $scope.currentUser = session.user;

    $scope.remove = function(user) {
      user.remove()
        .then(function() {
          notificationService.success('User deleted.');
          $state.go('users');
        })
        ['catch'](function() {
          notificationService.fail('Failed to delete user.');
        });
    };
  }

  DeleteUserController.$inject = ['$scope', 'user', 'session', 'notificationService', '$state'];

  app.controller('DeleteUserController', DeleteUserController);
})();
