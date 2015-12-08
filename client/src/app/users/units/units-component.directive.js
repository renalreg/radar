(function() {
  'use strict';

  var app = angular.module('radar.users.units');

  function controllerFactory(
    ModelListDetailController,
    $injector,
    store,
    firstPromise
  ) {
    function UserUnitsController($scope) {
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

    UserUnitsController.$inject = ['$scope'];
    UserUnitsController.prototype = Object.create(ModelListDetailController.prototype);

    return UserUnitsController;
  }

  controllerFactory.$inject = [
    'ModelListDetailController',
    '$injector',
    'store',
    'firstPromise'
  ];

  app.factory('UserUnitsController', controllerFactory);

  app.directive('userUnitsComponent', ['UserUnitsController', function(UserUnitsController) {
    return {
      scope: {
        user: '='
      },
      controller: UserUnitsController,
      templateUrl: 'app/users/units/units-component.html'
    };
  }]);
})();
