(function() {
  'use strict';

  var app = angular.module('radar.users');

  app.factory('NewUserController', ['ModelEditController', '$injector', 'store', '$state', function(ModelEditController, $injector, store, $state) {
    function NewUserController($scope) {
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

    NewUserController.$inject = ['$scope'];
    NewUserController.prototype = Object.create(ModelEditController.prototype);

    NewUserController.prototype.save = function() {
      return ModelEditController.prototype.save.call(this).then(function(user) {
        $state.go('user', {userId: user.id});
      });
    };

    return NewUserController;
  }]);

  app.directive('newUserComponent', ['NewUserController', function(NewUserController) {
    return {
      scope: {},
      controller: NewUserController,
      templateUrl: 'app/users/new/new-user-component.html'
    };
  }]);
})();
