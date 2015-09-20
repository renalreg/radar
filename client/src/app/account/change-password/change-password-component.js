(function() {
  'use strict';

  var app = angular.module('radar.account.changePassword');

  app.factory('ChangePasswordController', ['EditController', '$injector', function(EditController, $injector) {
    function ChangePasswordController($scope) {
      var self = this;

      $injector.invoke(EditController, self, {
        $scope: $scope,
        params: {}
      });

      self.load($scope.user);
    }

    ChangePasswordController.$inject = ['$scope'];
    ChangePasswordController.prototype = Object.create(EditController.prototype);

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
