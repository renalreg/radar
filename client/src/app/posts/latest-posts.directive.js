(function() {
  'use strict';

  var app = angular.module('radar.patients');

  app.factory('LatestPostsController', function(ListController, $injector) {
    function LatestPostsController($scope, store) {
      var self = this;

      $injector.invoke(ListController, self, {$scope: $scope});

      self.load(store.findMany('posts', {sort: '-publishedDate', perPage: 1, page: 1}));
    }

    LatestPostsController.prototype = Object.create(ListController.prototype);

    return LatestPostsController;
  });

  app.directive('latestPosts', function(LatestPostsController) {
    return {
      scope: {},
      controller: LatestPostsController,
      templateUrl: 'app/posts/latest-posts.html'
    };
  });
})();

