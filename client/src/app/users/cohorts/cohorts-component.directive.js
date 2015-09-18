(function() {
  'use strict';

  var app = angular.module('radar.users.cohorts');

  app.factory('UserCohortsController', function(ListDetailController) {
    function UserCohortsController($scope, $injector, store, firstPromise) {
      var self = this;

      $injector.invoke(ListDetailController, self, {
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

    UserCohortsController.prototype = Object.create(ListDetailController.prototype);

    return UserCohortsController;
  });

  app.directive('userCohortsComponent', function(UserCohortsController) {
    return {
      scope: {
        user: '='
      },
      controller: UserCohortsController,
      templateUrl: 'app/users/cohorts/cohorts-component.html'
    };
  });
})();
