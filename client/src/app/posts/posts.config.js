(function() {
  'use strict';

  var app = angular.module('radar.posts');

  app.config(['$stateProvider', function($stateProvider) {
    $stateProvider.state('posts', {
      url: '/news',
      templateUrl: 'app/posts/post-list.html',
      controller: 'PostListController',
      resolve: {
        posts: ['store', function(store) {
          return store.findMany('posts', {sort: '-publishedDate'});
        }]
      },
      data: {
        public: true
      }
    });
  }]);
})();
