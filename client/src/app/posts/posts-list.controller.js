(function() {
  'use strict';

  var app = angular.module('radar.dialysis');

  app.controller('PostListController', function($scope, posts) {
    $scope.posts = posts;
  });
})();
