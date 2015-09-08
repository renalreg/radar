(function() {
  'use strict';

  var app = angular.module('radar.posts');

  app.controller('PostListController', function($scope, posts) {
    $scope.posts = posts;
  });
})();
