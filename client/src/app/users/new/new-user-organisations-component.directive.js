(function() {
  'use strict';

  var app = angular.module('radar.users.new');

  app.factory('NewUserOrganisationsController', ['ListEditController', '$injector', 'store', function(ListEditController, $injector, store) {
    function NewUserOrganisationsController($scope) {
      var self = this;

      $injector.invoke(ListEditController, self, {
        $scope: $scope
      });

      self.load($scope.user.organisations);

      this.scope.appendOrganisation = angular.bind(this, this.appendOrganisation);
    }

    NewUserOrganisationsController.$inject = ['$scope'];
    NewUserOrganisationsController.prototype = Object.create(ListEditController.prototype);

    NewUserOrganisationsController.prototype.appendOrganisation = function() {
      this.append(store.create('user-organisations'));
    };

    return NewUserOrganisationsController;
  }]);

  app.directive('newUserOrganisationsComponent', ['NewUserOrganisationsController', function(NewUserOrganisationsController) {
    return {
      scope: {
        user: '='
      },
      controller: NewUserOrganisationsController,
      templateUrl: 'app/users/new/new-user-organisations-component.html'
    };
  }]);
})();
