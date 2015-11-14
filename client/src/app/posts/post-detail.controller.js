(function() {
  'use strict';

  var app = angular.module('radar.posts');

  app.controller('PostDetailControler', ['$scope', 'post', '$sce', function($scope, post, $sce) {
    $scope.post = post;
    post.html = $sce.trustAsHtml(post.body);
  }]);
})();
