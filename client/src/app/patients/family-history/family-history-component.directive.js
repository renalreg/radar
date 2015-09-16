(function() {
  'use strict';

  var app = angular.module('radar.patients.genetics');

  app.factory('FamilyHistoryPermission', function(PatientDataPermission) {
    return PatientDataPermission;
  });

  app.factory('FamilyHistoryController', function(DetailController, FamilyHistoryPermission) {
    function FamilyHistoryController($scope, $injector, store) {
      var self = this;

      $injector.invoke(DetailController, self, {
        $scope: $scope,
        params: {
          permission: new FamilyHistoryPermission($scope.patient)
        }
      });

      self.load(store.findMany('family-history', {patient: $scope.patient.id}).then(function(familyHistoryList) {
        if (familyHistoryList.length) {
          return familyHistoryList[0];
        } else {
          return null;
        }
      })).then(function() {
        self.view();
      });

      $scope.create = function() {
        var item = store.create('family-history', {patient: $scope.patient.id});
        self.edit(item);
      };
    }

    FamilyHistoryController.prototype = Object.create(DetailController.prototype);

    return FamilyHistoryController;
  });

  app.directive('familyHistoryComponent', function(FamilyHistoryController) {
    return {
      scope: {
        patient: '='
      },
      controller: FamilyHistoryController,
      templateUrl: 'app/patients/family-history/family-history-component.html'
    };
  });
})();
