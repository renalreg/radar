(function() {
  'use strict';

  var app = angular.module('radar.posts');

  app.config(function($stateProvider) {
    $stateProvider.state('posts', {
      url: '/news',
      templateUrl: 'app/posts/post-list.html',
      controller: 'PostListController'
    });
  });
})();
