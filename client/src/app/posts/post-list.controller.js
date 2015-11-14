(function() {
  'use strict';

  var app = angular.module('radar.posts');

  app.controller('PostListController', ['$scope', 'posts', '_', '$sce', function($scope, posts, _, $sce) {
    $scope.posts = posts;

    _.each(posts, function(post) {
      post.html = $sce.trustAsHtml(post.body);
    });
  }]);
})();
