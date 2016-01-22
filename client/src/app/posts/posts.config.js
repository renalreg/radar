(function() {
  'use strict';

  var app = angular.module('radar.posts');

  app.config(['$stateProvider', function($stateProvider) {
    $stateProvider.state('posts', {
      url: '/news',
      templateUrl: 'app/posts/post-list.html',
      controller: ['$scope', '$controller', 'PostListController', function($scope, $controller, PostListController) {
        $controller(PostListController, {$scope: $scope});
      }],
      data: {
        public: true
      }
    });

    $stateProvider.state('createPost', {
      url: '/news/create',
      templateUrl: 'app/posts/post-detail.html',
      controller: ['$scope', '$controller', 'PostDetailController', 'post', function($scope, $controller, PostDetailController, post) {
        $scope.post = post;
        $controller(PostDetailController, {$scope: $scope});
      }],
      resolve: {
        post: ['store', function(store) {
          return store.create('posts');
        }]
      }
    });

    $stateProvider.state('post', {
      url: '/news/:postId',
      templateUrl: 'app/posts/post-detail.html',
      controller: ['$scope', '$controller', 'PostDetailController', 'post', function($scope, $controller, PostDetailController, post) {
        $scope.post = post;
        $controller(PostDetailController, {$scope: $scope});
      }],
      resolve: {
        post: ['store', '$stateParams', function(store, $stateParams) {
          return store.findOne('posts', $stateParams.postId);
        }]
      },
      data: {
        public: true
      }
    });
  }]);
})();
