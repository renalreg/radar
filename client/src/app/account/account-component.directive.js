(function() {
  'use strict';

  var app = angular.module('radar.account');

  function controllerFactory(
    ModelEditController,
    $injector,
    notificationService
  ) {
    function AccountController($scope) {
      var self = this;

      $injector.invoke(ModelEditController, self, {
        $scope: $scope,
        params: {}
      });

      self.load($scope.user);
    }

    AccountController.$inject = ['$scope'];
    AccountController.prototype = Object.create(ModelEditController.prototype);

    AccountController.prototype.save = function() {
      return ModelEditController.prototype.save.call(this).then(function() {
        notificationService.success('Account updated.');
      });
    };

    return AccountController;
  }

  controllerFactory.$inject = [
    'ModelEditController',
    '$injector',
    'notificationService'
  ];

  app.factory('AccountController', controllerFactory);

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
