(function() {
  'use strict';

  var app = angular.module('radar.patients.familyHistory');

  function controllerFactory(
    ListEditController,
    $injector,
    firstPromise,
    store
  ) {
    function FamilyHistoryRelativesController($scope) {
      $injector.invoke(ListEditController, this, {$scope: $scope, params: {}});

      this.load(firstPromise([
        $scope.parent.relatives,
        store.findMany('family-history-relationships').then(function(relationships) {
          $scope.relationships = relationships;
        })
      ]));

      $scope.create = function() {
        $scope.parent.relatives.push({});
      };
    }

    FamilyHistoryRelativesController.$inject = ['$scope'];
    FamilyHistoryRelativesController.prototype = Object.create(ListEditController.prototype);

    return FamilyHistoryRelativesController;
  }

  controllerFactory.$inject = [
    'ListEditController',
    '$injector',
    'firstPromise',
    'store'
  ];

  app.factory('FamilyHistoryRelativesController', controllerFactory);

  app.directive('familyHistoryRelativesComponent', ['FamilyHistoryRelativesController', function(FamilyHistoryRelativesController) {
    return {
      scope: {
        parent: '=familyHistory'
      },
      controller: FamilyHistoryRelativesController,
      templateUrl: 'app/patients/family-history/relatives-component.html'
    };
  }]);
})();
