(function() {
  'use strict';

  var app = angular.module('radar.users');

  app.config(['$stateProvider', function($stateProvider) {
    $stateProvider.state('users', {
      url: '/users',
      templateUrl: 'app/users/user-list.html',
      controller: ['$scope', '$controller', 'UserListController', function($scope, $controller, UserListController) {
        $controller(UserListController, {$scope: $scope});
      }]
    });

    $stateProvider.state('createUser', {
      url: '/users/create',
      templateUrl: 'app/users/create-user.html'
    });

    $stateProvider.state('user', {
      url: '/users/:userId',
      templateUrl: 'app/users/user-detail.html',
      controller: ['$scope', 'user', 'session', function($scope, user, session) {
        $scope.user = user;
        $scope.currentUser = session.user;
      }],
      resolve: {
        user: ['$stateParams', 'store', function($stateParams, store) {
          return store.findOne('users', $stateParams.userId);
        }]
      }
    });

    $stateProvider.state('deleteUser', {
      url: '/users/:userId/delete',
      templateUrl: 'app/users/delete-user.html',
      controller: 'DeleteUserController',
      resolve: {
        user: ['$stateParams', 'store', function($stateParams, store) {
          return store.findOne('users', $stateParams.userId);
        }]
      }
    });
  }]);
})();
