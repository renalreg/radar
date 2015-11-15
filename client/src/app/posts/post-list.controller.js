(function() {
  'use strict';

  var app = angular.module('radar.posts');

  app.controller('PostListController', ['$scope', 'posts', '_', '$sce', function($scope, posts, _, $sce) {
    $scope.posts = posts;
  }]);
})();
