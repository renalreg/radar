(function() {
  'use strict';

  var app = angular.module('radar.users.units');

  app.factory('UserUnitsController', function(ModelListDetailController) {
    function UserUnitsController($scope, $injector, store, firstPromise) {
      var self = this;

      $injector.invoke(ModelListDetailController, self, {
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

    UserUnitsController.prototype = Object.create(ModelListDetailController.prototype);

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
