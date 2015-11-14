(function() {
  'use strict';

  var app = angular.module('radar.posts');

  app.factory('PostController', ['ModelEditController', '$injector', function(ModelEditController, $injector) {
    function PostController($scope) {
      var self = this;

      $injector.invoke(ModelEditController, self, {
        $scope: $scope,
        params: {}
      });

      self.load($scope.post);
    }

    PostController.$inject = ['$scope'];
    PostController.prototype = Object.create(ModelEditController.prototype);

    PostController.prototype.save = function() {
      var self = this;

      return ModelEditController.prototype.save.call(self).then(function(post) {
        // Update the post to the post we just saved, this is only needed when
        // saving a new post
        self.scope.post = post;
      });
    };

    return PostController;
  }]);

  app.directive('postComponent', ['PostController', function(PostController) {
    return {
      scope: {
        post: '='
      },
      controller: PostController,
      templateUrl: 'app/posts/post-component.html'
    };
  }]);
})();
