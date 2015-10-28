(function() {
  'use strict';

  var app = angular.module('radar.users.new');

  app.factory('NewUserController', ['ModelEditController', '$injector', 'store', function(ModelEditController, $injector, store) {
    function NewUserController($scope) {
      var self = this;

      $injector.invoke(ModelEditController, self, {
        $scope: $scope,
        params: {}
      });

      self.load(store.create('users'));
    }

    NewUserController.$inject = ['$scope'];
    NewUserController.prototype = Object.create(ModelEditController.prototype);

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
