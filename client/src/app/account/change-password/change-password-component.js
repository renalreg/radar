(function() {
  'use strict';

  var app = angular.module('radar.account.changePassword');

  app.factory('ChangePasswordController', ['EditController', '$injector', 'notificationService', function(EditController, $injector, notificationService) {
    function ChangePasswordController($scope) {
      var self = this;

      $injector.invoke(EditController, self, {
        $scope: $scope,
        params: {}
      });

      $scope.data = {};

      self.load($scope.user);
    }

    ChangePasswordController.$inject = ['$scope'];
    ChangePasswordController.prototype = Object.create(EditController.prototype);

    ChangePasswordController.prototype.save = function() {
      var self = this;

      // Set the user's password
      self.scope.item.password = self.scope.data.password;

      return EditController.prototype.save.call(this).then(function() {
        notificationService.success('Your password has been updated.');
        self.scope.data = {};
      });
    };

    return ChangePasswordController;
  }]);

  app.directive('changePasswordComponent', ['ChangePasswordController', function(ChangePasswordController) {
    return {
      scope: {
        user: '='
      },
      controller: ChangePasswordController,
      templateUrl: 'app/account/change-password/change-password-component.html'
    };
  }]);
})();
