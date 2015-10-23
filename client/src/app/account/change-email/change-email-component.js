(function() {
  'use strict';

  var app = angular.module('radar.account.changeEmail');

  app.factory('ChangeEmailController', ['EditController', '$injector', 'notificationService', function(EditController, $injector, notificationService) {
    function ChangeEmailController($scope) {
      var self = this;

      $injector.invoke(EditController, self, {
        $scope: $scope,
        params: {}
      });

      $scope.data = {};

      self.load($scope.user);
    }

    ChangeEmailController.$inject = ['$scope'];
    ChangeEmailController.prototype = Object.create(EditController.prototype);

    ChangeEmailController.prototype.save = function() {
      var self = this;

      // Set the user's email
      self.scope.item.email = self.scope.data.email;

      return EditController.prototype.save.call(this).then(function() {
        notificationService.success('Your email has been updated.');
        self.scope.data = {};
      });
    };

    return ChangeEmailController;
  }]);

  app.directive('changeEmailComponent', ['ChangeEmailController', function(ChangeEmailController) {
    return {
      scope: {
        user: '='
      },
      controller: ChangeEmailController,
      templateUrl: 'app/account/change-email/change-email-component.html'
    };
  }]);
})();
