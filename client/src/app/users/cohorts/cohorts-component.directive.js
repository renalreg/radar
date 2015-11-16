(function() {
  'use strict';

  var app = angular.module('radar.users.cohorts');

  function controllerFactory(
    ModelListDetailController,
    $injector,
    store,
    firstPromise
  ) {
    function UserCohortsController($scope) {
      var self = this;

      $injector.invoke(ModelListDetailController, self, {
        $scope: $scope,
        params: {}
      });

      self.load(firstPromise([
        $scope.user.cohorts,
        store.findMany('cohort-user-roles').then(function(roles) {
          $scope.roles = roles;
        })
      ]));

      $scope.create = function() {
        self.edit(store.create('cohort-users', {user: $scope.user.id}));
      };
    }

    UserCohortsController.$inject = ['$scope'];
    UserCohortsController.prototype = Object.create(ModelListDetailController.prototype);

    return UserCohortsController;
  }

  controllerFactory.$inject = [
    'ModelListDetailController',
    '$injector',
    'store',
    'firstPromise'
  ];

  app.factory('UserCohortsController', controllerFactory);

  app.directive('userCohortsComponent', ['UserCohortsController', function(UserCohortsController) {
    return {
      scope: {
        user: '='
      },
      controller: UserCohortsController,
      templateUrl: 'app/users/cohorts/cohorts-component.html'
    };
  }]);
})();
