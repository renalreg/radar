(function() {
  'use strict';

  var app = angular.module('radar.patients.genetics');

  app.factory('FamilyHistoryPermission', ['PatientObjectPermission', function(PatientObjectPermission) {
    return PatientObjectPermission;
  }]);

  app.factory('FamilyHistoryController', ['DetailController', 'FamilyHistoryPermission', '$injector', 'store', function(DetailController, FamilyHistoryPermission, $injector, store) {
    function FamilyHistoryController($scope) {
      var self = this;

      $injector.invoke(DetailController, self, {
        $scope: $scope,
        params: {
          permission: new FamilyHistoryPermission($scope.patient)
        }
      });

      self.load(store.findFirst('family-history', {patient: $scope.patient.id, cohort: $scope.cohort.id})).then(function() {
        self.view();
      });

      $scope.create = function() {
        var item = store.create('family-history', {patient: $scope.patient.id, cohort: $scope.cohort});
        self.edit(item);
      };
    }

    FamilyHistoryController.$inject = ['$scope'];
    FamilyHistoryController.prototype = Object.create(DetailController.prototype);

    return FamilyHistoryController;
  }]);

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
