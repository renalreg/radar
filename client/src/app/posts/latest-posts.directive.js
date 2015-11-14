(function() {
  'use strict';

  var app = angular.module('radar.patients');

  app.factory('LatestPostsController', ['ListController', '$injector', 'store', function(ListController, $injector, store) {
    function LatestPostsController($scope) {
      var self = this;

      $injector.invoke(ListController, self, {$scope: $scope});

      self.load(store.findMany('posts', {sort: '-publishedDate', perPage: 1, page: 1}).then(function(posts) {
        _.each(posts, function(post) {
          post.html = $sce.trustAsHtml(post.body);
        });

        return posts;
      }));
    }

    LatestPostsController.$inject = ['$scope'];

    LatestPostsController.prototype = Object.create(ListController.prototype);

    return LatestPostsController;
  }]);

  app.directive('latestPosts', ['LatestPostsController', function(LatestPostsController) {
    return {
      scope: {},
      controller: LatestPostsController,
      templateUrl: 'app/posts/latest-posts.html'
    };
  }]);
})();
