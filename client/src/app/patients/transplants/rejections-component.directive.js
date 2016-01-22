(function() {
  'use strict';

  var app = angular.module('radar.patients.transplants');

  function controllerFactory(
    ListEditController,
    $injector
  ) {
    function TransplantRejectionsController($scope) {
      $injector.invoke(ListEditController, this, {$scope: $scope, params: {}});
      this.load($scope.parent.rejections);

      $scope.create = function() {
        $scope.parent.rejections.push({});
      };
    }

    TransplantRejectionsController.$inject = ['$scope'];
    TransplantRejectionsController.prototype = Object.create(ListEditController.prototype);

    return TransplantRejectionsController;
  }

  controllerFactory.$inject = [
    'ListEditController',
    '$injector'
  ];

  app.factory('TransplantRejectionsController', controllerFactory);

  app.directive('transplantRejectionsComponent', ['TransplantRejectionsController', function(TransplantRejectionsController) {
    return {
      scope: {
        parent: '=transplant'
      },
      controller: TransplantRejectionsController,
      templateUrl: 'app/patients/transplants/rejections-component.html'
    };
  }]);
})();
