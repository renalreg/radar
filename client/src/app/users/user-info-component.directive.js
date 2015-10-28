(function() {
  'use strict';

  var app = angular.module('radar.users');

  app.factory('UserInfoController', ['ModelDetailController', '$injector', function(ModelDetailController, $injector) {
    function UserInfoController($scope) {
      var self = this;

      $injector.invoke(ModelDetailController, self, {
        $scope: $scope,
        params: {}
      });

      self.load($scope.user).then(function() {
        self.view();
      });
    }

    UserInfoController.$inject = ['$scope'];
    UserInfoController.prototype = Object.create(ModelDetailController.prototype);

    return UserInfoController;
  }]);

  app.directive('userInfoComponent', ['UserInfoController', function(UserInfoController) {
    return {
      scope: {
        user: '='
      },
      controller: UserInfoController,
      templateUrl: 'app/users/user-info-component.html'
    };
  }]);
})();
