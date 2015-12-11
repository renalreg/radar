(function() {
  'use strict';

  var app = angular.module('radar.patients.transplants');

  function controllerFactory(
    ListEditController,
    $injector
  ) {
    function TransplantBiopsiesController($scope) {
      $injector.invoke(ListEditController, this, {$scope: $scope, params: {}});
      this.load($scope.parent.biopsies);

      $scope.create = function() {
        $scope.parent.biopsies.push({});
      };
    }

    TransplantBiopsiesController.$inject = ['$scope'];
    TransplantBiopsiesController.prototype = Object.create(ListEditController.prototype);

    return TransplantBiopsiesController;
  }

  controllerFactory.$inject = [
    'ListEditController',
    '$injector'
  ];

  app.factory('TransplantBiopsiesController', controllerFactory);

  app.directive('transplantBiopsiesComponent', ['TransplantBiopsiesController', function(TransplantBiopsiesController) {
    return {
      scope: {
        parent: '=transplant'
      },
      controller: TransplantBiopsiesController,
      templateUrl: 'app/patients/transplants/biopsies-component.html'
    };
  }]);
})();
