(function() {
  'use strict';

  var app = angular.module('radar.posts');

  app.factory('LatestPostsController', ['ListController', '$injector', 'store', '$sce', '_', function(ListController, $injector, store, $sce, _) {
    function LatestPostsController($scope) {
      var self = this;

      $injector.invoke(ListController, self, {$scope: $scope});

      self.load(store.findMany('posts', {sort: '-publishedDate', perPage: 1, page: 1}));
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
