(function() {
  'use strict';

  var app = angular.module('radar.resultSpecs');

  function controllerFactory(
    ModelListDetailController,
    $injector,
    store
  ) {
    function ResultSpecsController($scope) {
      var self = this;

      $injector.invoke(ModelListDetailController, self, {
        $scope: $scope,
        params: {}
      });

      self.load(store.findMany('result-specs'));
    }

    ResultSpecsController.$inject = ['$scope'];
    ResultSpecsController.prototype = Object.create(ModelListDetailController.prototype);

    return ResultSpecsController;
  }

  controllerFactory.$inject = [
    'ModelListDetailController',
    '$injector',
    'store'
  ];

  app.factory('ResultSpecsController', controllerFactory);

  app.directive('resultSpecsComponent', ['ResultSpecsController', function(ResultSpecsController) {
    return {
      controller: ResultSpecsController,
      templateUrl: 'app/result-specs/result-specs-component.html'
    };
  }]);
})();
