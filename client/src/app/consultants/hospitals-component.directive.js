(function() {
  'use strict';

  var app = angular.module('radar.consultants');

  function controllerFactory(
    ListEditController,
    $injector
  ) {
    function ConsultantHospitalsController($scope) {
      $injector.invoke(ListEditController, this, {$scope: $scope, params: {}});
      this.load($scope.parent.groups);

      $scope.create = function() {
        $scope.parent.groups.push({});
      };
    }

    ConsultantHospitalsController.$inject = ['$scope'];
    ConsultantHospitalsController.prototype = Object.create(ListEditController.prototype);

    return ConsultantHospitalsController;
  }

  controllerFactory.$inject = [
    'ListEditController',
    '$injector'
  ];

  app.factory('ConsultantHospitalsController', controllerFactory);

  app.directive('consultantHospitalsComponent', ['ConsultantHospitalsController', function(ConsultantHospitalsController) {
    return {
      scope: {
        parent: '=consultant'
      },
      controller: ConsultantHospitalsController,
      templateUrl: 'app/consultants/hospitals-component.html'
    };
  }]);
})();
