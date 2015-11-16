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

    $stateProvider.state('newUser', {
      url: '/users/new',
      templateUrl: 'app/users/new-user.html'
    });

    $stateProvider.state('user', {
      url: '/users/:userId',
      templateUrl: 'app/users/user-detail.html',
      controller: ['$scope', 'user', function($scope, user) {
        $scope.user = user;
      }],
      resolve: {
        user: ['$stateParams', 'store', function($stateParams, store) {
          return store.findOne('users', $stateParams.userId);
        }]
      }
    });
  }]);
})();
