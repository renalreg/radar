(function() {
  'use strict';

  var app = angular.module('radar.dialysis');

  app.factory('DiseaseGroupController', function(ListDetailController) {
    function DiseaseGroupController($scope, $injector, store) {
      var self = this;

      $injector.invoke(ListDetailController, self, {$scope: $scope, params: {}});

      self.load($scope.patient.diseaseGroups);

      $scope.create = function() {
        self.edit(store.create('patient-disease-groups', {
          patientId: $scope.patient.id
        }));
      };
    }

    DiseaseGroupController.prototype = Object.create(ListDetailController.prototype);

    return DiseaseGroupController;
  });

  app.directive('diseaseGroupComponent', function(DiseaseGroupController) {
    return {
      scope: {
        patient: '='
      },
      controller: DiseaseGroupController,
      templateUrl: 'app/disease-groups/disease-group-component.html'
    };
  });
})();

