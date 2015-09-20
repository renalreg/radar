(function() {
  'use strict';

  var app = angular.module('radar.account.changeEmail');

  app.factory('ChangeEmailController', ['EditController', '$injector', function(EditController, $injector) {
    function ChangeEmailController($scope) {
      var self = this;

      $injector.invoke(EditController, self, {
        $scope: $scope,
        params: {}
      });

      self.load($scope.user);
    }

    ChangeEmailController.$inject = ['$scope'];
    ChangeEmailController.prototype = Object.create(EditController.prototype);

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
