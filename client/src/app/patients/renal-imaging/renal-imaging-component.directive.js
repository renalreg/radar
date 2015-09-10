(function() {
  'use strict';

  var app = angular.module('radar.patients.renalImaging');

  app.factory('RenalImagingPermission', function(PatientFacilityDataPermission) {
    return PatientFacilityDataPermission;
  });

  app.factory('RenalImagingController', function(ListDetailController, RenalImagingPermission, kidneyTypes, imagingTypes) {
    function RenalImagingController($scope, $injector, store) {
      var self = this;

      $injector.invoke(ListDetailController, self, {
        $scope: $scope,
        params: {
          permission: new RenalImagingPermission($scope.patient)
        }
      });

      $scope.kidneyTypes = kidneyTypes;
      $scope.imagingTypes = imagingTypes;

      self.load(store.findMany('renal-imaging', {patientId: $scope.patient.id}));

      $scope.create = function() {
        var item = store.create('renal-imaging', {patientId: $scope.patient.id});
        self.edit(item);
      };

      $scope.log = function() {
        console.log($scope);
      };
    }

    RenalImagingController.prototype = Object.create(ListDetailController.prototype);

    return RenalImagingController;
  });

  app.directive('renalImagingComponent', function(RenalImagingController) {
    return {
      scope: {
        patient: '='
      },
      controller: RenalImagingController,
      templateUrl: 'app/patients/renal-imaging/renal-imaging-component.html'
    };
  });
})();
