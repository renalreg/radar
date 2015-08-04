(function() {
  'use strict';

  var app = angular.module('radar.posts');

  app.controller('PostDetailController', function($scope, post) {
    $scope.post = post;
  });
})();
