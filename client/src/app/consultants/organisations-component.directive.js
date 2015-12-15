(function() {
  'use strict';

  var app = angular.module('radar.consultants');

  function controllerFactory(
    ListEditController,
    $injector
  ) {
    function ConsultantOrganisationsController($scope) {
      $injector.invoke(ListEditController, this, {$scope: $scope, params: {}});
      this.load($scope.parent.organisationConsultants);

      $scope.create = function() {
        $scope.parent.organisationConsultants.push({});
      };
    }

    ConsultantOrganisationsController.$inject = ['$scope'];
    ConsultantOrganisationsController.prototype = Object.create(ListEditController.prototype);

    return ConsultantOrganisationsController;
  }

  controllerFactory.$inject = [
    'ListEditController',
    '$injector'
  ];

  app.factory('ConsultantOrganisationsController', controllerFactory);

  app.directive('consultantOrganisationsComponent', ['ConsultantOrganisationsController', function(ConsultantOrganisationsController) {
    return {
      scope: {
        parent: '=consultant'
      },
      controller: ConsultantOrganisationsController,
      templateUrl: 'app/consultants/organisations-component.html'
    };
  }]);
})();
