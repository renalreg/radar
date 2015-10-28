(function() {
  'use strict';

  var app = angular.module('radar.users');

  app.factory('NewUserController', ['EditController', '$injector', 'store', function(EditController, $injector, store) {
    function NewUserController($scope) {
      var self = this;

      $injector.invoke(EditController, self, {
        $scope: $scope,
        params: {}
      });

      self.load(store.create('users'));
    }

    NewUserController.$inject = ['$scope'];
    NewUserController.prototype = Object.create(EditController.prototype);

    return NewUserController;
  }]);

  app.directive('newUserComponent', ['NewUserController', function(NewUserController) {
    return {
      scope: {},
      controller: NewUserController,
      templateUrl: 'app/users/new-user-component.html'
    };
  }]);
})();
