(function() {
  'use strict';

  var app = angular.module('radar.posts');

  app.controller('PostEditControler', ['$scope', 'post', '$sce', function($scope, post, $sce) {
    $scope.post = post;

    $scope.$watch('post.body', function(body) {
      post.html = $sce.trustAsHtml(body);
    });
  }]);
})();
