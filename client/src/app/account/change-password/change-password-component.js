(function() {
  'use strict';

  var app = angular.module('radar.account.changePassword');

  app.factory('ChangePasswordController', function(EditController) {
    function ChangePasswordController($scope, $injector) {
      var self = this;

      $injector.invoke(EditController, self, {
        $scope: $scope,
        params: {}
      });

      self.load($scope.user);
    }

    ChangePasswordController.prototype = Object.create(EditController.prototype);

    return ChangePasswordController;
  });

  app.directive('changePasswordComponent', function(ChangePasswordController) {
    return {
      scope: {
        user: '='
      },
      controller: ChangePasswordController,
      templateUrl: 'app/account/change-password/change-password-component.html'
    };
  });
})();
