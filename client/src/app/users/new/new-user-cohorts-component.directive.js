(function() {
  'use strict';

  var app = angular.module('radar.users.new');

  app.factory('NewUserCohortsController', ['ListEditController', '$injector', 'store', function(ListEditController, $injector, store) {
    function NewUserCohortsController($scope) {
      $injector.invoke(ListEditController, this, {
        $scope: $scope
      });

      this.load($scope.user.cohorts);

      this.scope.appendCohort = angular.bind(this, this.appendCohort);
    }

    NewUserCohortsController.$inject = ['$scope'];
    NewUserCohortsController.prototype = Object.create(ListEditController.prototype);

    NewUserCohortsController.prototype.appendCohort = function() {
      this.append(store.create('user-cohorts'));
    };

    return NewUserCohortsController;
  }]);

  app.directive('newUserCohortsComponent', ['NewUserCohortsController', function(NewUserCohortsController) {
    return {
      scope: {
        user: '='
      },
      controller: NewUserCohortsController,
      templateUrl: 'app/users/new/new-user-cohorts-component.html'
    };
  }]);
})();
