(function() {
  'use strict';

  var app = angular.module('radar.account');

  app.factory('AccountController', function(EditController) {
    function AccountController($scope, $injector) {
      var self = this;

      $injector.invoke(EditController, self, {
        $scope: $scope,
        params: {}
      });

      self.load($scope.user);
    }

    AccountController.prototype = Object.create(EditController.prototype);

    return AccountController;
  });

  app.directive('accountComponent', function(AccountController) {
    return {
      scope: {
        user: '='
      },
      controller: AccountController,
      templateUrl: 'app/account/account-component.html'
    };
  });
})();
