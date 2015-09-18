(function() {
  'use strict';

  var app = angular.module('radar.account.changeEmail');

  app.factory('ChangeEmailController', function(EditController) {
    function ChangeEmailController($scope, $injector) {
      var self = this;

      $injector.invoke(EditController, self, {
        $scope: $scope,
        params: {}
      });

      self.load($scope.user);
    }

    ChangeEmailController.prototype = Object.create(EditController.prototype);

    return ChangeEmailController;
  });

  app.directive('changeEmailComponent', function(ChangeEmailController) {
    return {
      scope: {
        user: '='
      },
      controller: ChangeEmailController,
      templateUrl: 'app/account/change-email/change-email-component.html'
    };
  });
})();
