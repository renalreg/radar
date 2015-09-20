(function() {
  'use strict';

  var app = angular.module('radar.posts');

  app.controller('PostListController', ['$scope', 'posts', function($scope, posts) {
    $scope.posts = posts;
  }]);
})();
