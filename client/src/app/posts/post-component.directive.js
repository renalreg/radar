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
