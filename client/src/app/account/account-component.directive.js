(function() {
  'use strict';

  var app = angular.module('radar.account');

  app.factory('AccountController', ['EditController', '$injector', function(EditController, $injector) {
    function AccountController($scope) {
      var self = this;

      $injector.invoke(EditController, self, {
        $scope: $scope,
        params: {}
      });

      self.load($scope.user);
    }

    AccountController.$inject = ['$scope'];
    AccountController.prototype = Object.create(EditController.prototype);

    return AccountController;
  }]);

  app.directive('accountComponent', ['AccountController', function(AccountController) {
    return {
      scope: {
        user: '='
      },
      controller: AccountController,
      templateUrl: 'app/account/account-component.html'
    };
  }]);
})();
