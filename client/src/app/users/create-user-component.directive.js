(function() {
  'use strict';

  var app = angular.module('radar.users');

  app.factory('CreateUserController', ['ModelEditController', '$injector', 'store', '$state', function(ModelEditController, $injector, store, $state) {
    function CreateUserController($scope) {
      var self = this;

      $injector.invoke(ModelEditController, self, {
        $scope: $scope,
        params: {}
      });

      self.load(store.create('users', {
        isAdmin: false,
        forcePasswordChange: true
      }));
    }

    CreateUserController.$inject = ['$scope'];
    CreateUserController.prototype = Object.create(ModelEditController.prototype);

    CreateUserController.prototype.save = function() {
      return ModelEditController.prototype.save.call(this).then(function(user) {
        $state.go('user', {userId: user.id});
      });
    };

    return CreateUserController;
  }]);

  app.directive('createUserComponent', ['CreateUserController', function(CreateUserController) {
    return {
      scope: {},
      controller: CreateUserController,
      templateUrl: 'app/users/create-user-component.html'
    };
  }]);
})();
