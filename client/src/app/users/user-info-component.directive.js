(function() {
  'use strict';

  var app = angular.module('radar.users');

  app.factory('UserInfoController', function(DetailController, $injector) {
    function UserInfoController($scope) {
      var self = this;

      $injector.invoke(DetailController, self, {
        $scope: $scope,
        params: {}
      });

      self.load($scope.user).then(function() {
        self.view();
      });
    }

    UserInfoController.prototype = Object.create(DetailController.prototype);

    return UserInfoController;
  });

  app.directive('userInfoComponent', function(UserInfoController) {
    return {
      scope: {
        user: '='
      },
      controller: UserInfoController,
      templateUrl: 'app/users/user-info-component.html'
    };
  });
})();
