(function() {
  'use strict';

  var app = angular.module('radar.account.changeEmail');

  function controllerFactory(
    ModelEditController,
    $injector,
    notificationService
  ) {
    function ChangeEmailController($scope) {
      var self = this;

      $injector.invoke(ModelEditController, self, {
        $scope: $scope,
        params: {}
      });

      $scope.data = {};

      self.load($scope.user);
    }

    ChangeEmailController.$inject = ['$scope'];
    ChangeEmailController.prototype = Object.create(ModelEditController.prototype);

    ChangeEmailController.prototype.save = function() {
      var self = this;

      // Set the user's email
      self.scope.item.email = self.scope.data.email;

      return ModelEditController.prototype.save.call(this).then(function() {
        notificationService.success('Your email has been updated.');
        self.scope.data = {};
      });
    };

    return ChangeEmailController;
  }

  controllerFactory.$inject = [
    'ModelEditController',
    '$injector',
    'notificationService'
  ];

  app.factory('ChangeEmailController', controllerFactory);

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
