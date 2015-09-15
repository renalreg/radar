(function() {
  'use strict';

  var app = angular.module('radar.patients.renalImaging');

  app.factory('RenalImagingPermission', function(PatientDataSourceObjectPermission) {
    return PatientDataSourceObjectPermission;
  });

  app.factory('RenalImagingController', function(ListDetailController, RenalImagingPermission, firstPromise) {
    function RenalImagingController($scope, $injector, store) {
      var self = this;

      $injector.invoke(ListDetailController, self, {
        $scope: $scope,
        params: {
          permission: new RenalImagingPermission($scope.patient)
        }
      });

      self.load(firstPromise([
        store.findMany('renal-imaging', {patient: $scope.patient.id}),
        store.findMany('renal-imaging-types').then(function(imagingTypes) {
          $scope.imagingTypes = imagingTypes;
        }),
        store.findMany('renal-imaging-kidney-types').then(function(kidneyTypes) {
          $scope.kidneyTypes = kidneyTypes;
        })
      ]));

      $scope.create = function() {
        var item = store.create('renal-imaging', {patient: $scope.patient.id});
        self.edit(item);
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
