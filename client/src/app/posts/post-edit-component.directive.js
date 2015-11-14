(function() {
  'use strict';

  var app = angular.module('radar.posts');

  app.factory('PostEditComponentController', ['ModelEditController', '$injector', function(ModelEditController, $injector) {
    function PostEditComponentController($scope) {
      var self = this;

      $injector.invoke(ModelEditController, self, {
        $scope: $scope,
        params: {}
      });

      self.load($scope.post);
    }

    PostEditComponentController.$inject = ['$scope'];
    PostEditComponentController.prototype = Object.create(ModelEditController.prototype);

    PostEditComponentController.prototype.save = function() {
      var self = this;

      return ModelEditController.prototype.save.call(self).then(function(post) {
        // Update the post to the post we just saved, this is only needed when
        // saving a new post
        self.scope.post = post;
      });
    };

    return PostEditComponentController;
  }]);

  app.directive('postEditComponent', ['PostEditComponentController', function(PostEditComponentController) {
    return {
      scope: {
        post: '='
      },
      controller: PostEditComponentController,
      templateUrl: 'app/posts/post-edit-component.html'
    };
  }]);
})();
