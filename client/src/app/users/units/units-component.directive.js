(function() {
  'use strict';

  var app = angular.module('radar.users.units');

  app.factory('UserUnitsController', function(ListDetailController) {
    function UserUnitsController($scope, $injector, store, firstPromise) {
      var self = this;

      $injector.invoke(ListDetailController, self, {
        $scope: $scope,
        params: {}
      });

      self.load(firstPromise([
        $scope.user.organisations,
        store.findMany('organisation-user-roles').then(function(roles) {
          $scope.roles = roles;
        })
      ]));

      $scope.create = function() {
        self.edit(store.create('organisation-users', {user: $scope.user.id}));
      };
    }

    UserUnitsController.prototype = Object.create(ListDetailController.prototype);

    return UserUnitsController;
  });

  app.directive('userUnitsComponent', function(UserUnitsController) {
    return {
      scope: {
        user: '='
      },
      controller: UserUnitsController,
      templateUrl: 'app/users/units/units-component.html'
    };
  });
})();
