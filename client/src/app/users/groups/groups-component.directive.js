(function() {
  'use strict';

  var app = angular.module('radar.users.groups');

  function controllerFactory(
    ModelListDetailController,
    $injector,
    store,
    firstPromise
  ) {
    function UserGroupsController($scope) {
      var self = this;

      $injector.invoke(ModelListDetailController, self, {
        $scope: $scope,
        params: {}
      });

      self.load(firstPromise([
        $scope.user.groups,
        store.findMany('roles').then(function(roles) {
          $scope.roles = roles;
        })
      ]));

      $scope.create = function() {
        self.edit(store.create('group-users', {user: $scope.user.id}));
      };
    }

    UserGroupsController.$inject = ['$scope'];
    UserGroupsController.prototype = Object.create(ModelListDetailController.prototype);

    return UserGroupsController;
  }

  controllerFactory.$inject = [
    'ModelListDetailController',
    '$injector',
    'store',
    'firstPromise'
  ];

  app.factory('UserGroupsController', controllerFactory);

  app.directive('userGroupsComponent', ['UserGroupsController', function(UserGroupsController) {
    return {
      scope: {
        user: '='
      },
      controller: UserGroupsController,
      templateUrl: 'app/users/groups/groups-component.html'
    };
  }]);
})();
