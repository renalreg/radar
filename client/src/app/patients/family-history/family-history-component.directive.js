(function() {
  'use strict';

  var app = angular.module('radar.patients.familyHistory');

  app.factory('FamilyHistoryPermission', ['PatientObjectPermission', function(PatientObjectPermission) {
    return PatientObjectPermission;
  }]);

  function controllerFactory(
    ModelDetailController,
    FamilyHistoryPermission,
    $injector,
    store
  ) {
    function FamilyHistoryController($scope) {
      var self = this;

      $injector.invoke(ModelDetailController, self, {
        $scope: $scope,
        params: {
          permission: new FamilyHistoryPermission($scope.patient)
        }
      });

      self.load(store.findFirst('family-histories', {patient: $scope.patient.id, cohort: $scope.cohort.id})).then(function() {
        self.view();
      });

      $scope.create = function() {
        var item = store.create('family-histories', {patient: $scope.patient.id, cohort: $scope.cohort});
        self.edit(item);
      };
    }

    FamilyHistoryController.$inject = ['$scope'];
    FamilyHistoryController.prototype = Object.create(ModelDetailController.prototype);

    return FamilyHistoryController;
  }

  controllerFactory.$inject = [
    'ModelDetailController',
    'FamilyHistoryPermission',
    '$injector',
    'store'
  ];

  app.factory('FamilyHistoryController', controllerFactory);

  app.directive('familyHistoryComponent', ['FamilyHistoryController', function(FamilyHistoryController) {
    return {
      scope: {
        patient: '=',
        cohort: '='
      },
      controller: FamilyHistoryController,
      templateUrl: 'app/patients/family-history/family-history-component.html'
    };
  }]);
})();
