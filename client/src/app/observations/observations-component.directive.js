(function() {
  'use strict';

  var app = angular.module('radar.observations');

  function controllerFactory(
    ModelListDetailController,
    $injector,
    store
  ) {
    function ObservationsController($scope) {
      var self = this;

      $injector.invoke(ModelListDetailController, self, {
        $scope: $scope,
        params: {}
      });

      self.load(store.findMany('observations'));
    }

    ObservationsController.$inject = ['$scope'];
    ObservationsController.prototype = Object.create(ModelListDetailController.prototype);

    return ObservationsController;
  }

  controllerFactory.$inject = [
    'ModelListDetailController',
    '$injector',
    'store'
  ];

  app.factory('ObservationsController', controllerFactory);

  app.directive('observationsComponent', ['ObservationsController', function(ObservationsController) {
    return {
      controller: ObservationsController,
      templateUrl: 'app/observations/observations-component.html'
    };
  }]);
})();
